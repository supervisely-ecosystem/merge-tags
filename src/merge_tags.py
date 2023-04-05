from typing import List
import supervisely as sly
import src.globals as g


def get_merged_project_meta(tag_metas):
    dst_project_meta = g.project_meta.clone(tag_metas=tag_metas)
    return dst_project_meta


def get_merged_tag_metas(config):
    dst_tag_metas = []
    to_skip = set()
    for first_name, second_names in config.items():
        for second_name in second_names:
            to_skip.add(second_name)
    for first_name, second_names in config.items():
        if len(second_names) > 0:
            to_skip.discard(first_name)

    for first_name, second_names in config.items():
        if first_name in to_skip:
            continue
        first = g.tag_metas.get(first_name)
        for second_name in second_names:
            second = g.tag_metas.get(second_name)
            if (
                first.applicable_to != second.applicable_to
                and first.applicable_to != sly.TagApplicableTo.ALL
            ):
                first = first.clone(applicable_to=sly.TagApplicableTo.ALL)
            first_possible_values = set(
                [] if first.possible_values is None else first.possible_values
            )
            second_possible_values = set(
                [] if second.possible_values is None else second.possible_values
            )
            first_possible_values = first_possible_values.union(second_possible_values)
            first = first.clone(
                possible_values=None
                if len(first_possible_values) == 0
                else list(first_possible_values)
            )
        dst_tag_metas.append(first)
    return sly.TagMetaCollection(dst_tag_metas)


def create_project(project_meta):
    name = g.project_info.name + "(merged tags)"
    project = g.api.project.create(
        g.workspace_id,
        name,
        type=g.project_info.type,
        change_name_if_conflict=True,
        description=g.project_info.description,
    )
    g.api.project.update_meta(project.id, project_meta.to_json())
    return project


def update_tags(tags: sly.TagCollection, config, tag_metas: sly.TagMetaCollection):
    updated_tags = {}
    for first_name, second_names in config.items():
        if tag_metas.get(first_name) is None:
            continue
        first_tags = [tag for tag in tags if tag.name == first_name]
        second_tags = [tag for tag in tags if tag.name in second_names]
        tag_meta = tag_metas.get(first_name)
        updated_tags[first_name] = {}
        for tag in [*first_tags, *second_tags]:
            if tag.value in updated_tags[first_name]:
                updated_tags[first_name][tag.value].append(sly.Tag(tag_meta, tag.value))
            else:
                updated_tags[first_name][tag.value] = [sly.Tag(tag_meta, tag.value)]

    updated_tags_list = []
    for tag_name in updated_tags.keys():
        for tags in updated_tags[tag_name].values():
            for tag in tags:
                updated_tags_list.append(tag)

    return sly.TagCollection(updated_tags_list)


def update_video_tags(
    video_tags: sly.VideoTagCollection, config, tag_metas: sly.TagMetaCollection
):
    updated_tags = {}
    for first_name, second_names in config.items():
        if tag_metas.get(first_name) is None:
            continue
        first_tags = [tag for tag in video_tags if tag.name == first_name]
        second_tags = [tag for tag in video_tags if tag.name in second_names]
        tag_meta = tag_metas.get(first_name)
        updated_tags[first_name] = {}
        for tag in [*first_tags, *second_tags]:
            if tag.value in updated_tags[first_name]:
                updated_tags[first_name][tag.value].append(
                    sly.VideoTag(tag_meta, tag.value, tag.frame_range)
                )
            else:
                updated_tags[first_name][tag.value] = [
                    sly.VideoTag(tag_meta, tag.value, tag.frame_range)
                ]

    for tag_name in updated_tags.keys():
        for value, tags in updated_tags[tag_name].items():
            frame_tags = [tag for tag in tags if tag.frame_range is not None]
            sorted_tags = sorted(frame_tags, key=lambda tag: tag.frame_range[0])
            merged_tags = sorted_tags[:1]
            for tag in sorted_tags[1:]:
                if tag.frame_range[0] <= merged_tags[-1].frame_range[1]:
                    merged_tags[-1].frame_range[1] = max(
                        merged_tags[-1].frame_range[1], tag.frame_range[1]
                    )
                else:
                    merged_tags.append(tag)
            frameless_tags = [tag for tag in tags if tag.frame_range is None]
            if frameless_tags:
                merged_tags.append(frameless_tags[0])
            updated_tags[tag_name][value] = merged_tags

    updated_tags_list = []
    for tag_name in updated_tags.keys():
        for tags in updated_tags[tag_name].values():
            for tag in tags:
                updated_tags_list.append(tag)

    return sly.VideoTagCollection(updated_tags_list)


def update_labels(labels: List[sly.Label], config, dst_tag_metas):
    updated_labels = []
    for label in labels:
        updated_tags = update_tags(label.tags, config, dst_tag_metas)
        updated_labels.append(label.clone(tags=updated_tags))
    return updated_labels


def update_video_objects(objects: List[sly.VideoObject], config, dst_tag_metas):
    updated_objects = []
    for object in objects:
        updated_tags = update_video_tags(object.tags, config, dst_tag_metas)
        updated_objects.append(object.clone(tags=updated_tags))
    return updated_objects


def convert_image_annotation(
    annotation: sly.Annotation, config, tag_metas: sly.TagMetaCollection
):
    updated_img_tags = update_tags(annotation.img_tags, config, tag_metas)
    updated_labels = update_labels(annotation.labels, config, tag_metas)
    return annotation.clone(img_tags=updated_img_tags, labels=updated_labels)


def convert_video_annotation(
    annotation: sly.VideoAnnotation, config, tag_metas: sly.TagMetaCollection
):
    updated_video_tags = update_video_tags(annotation.tags, config, tag_metas)
    updated_objects = update_video_objects(annotation.objects, config, tag_metas)
    return annotation.clone(tags=updated_video_tags, objects=updated_objects)


def run(config):
    dst_tag_metas = get_merged_tag_metas(config)
    dst_project_meta = get_merged_project_meta(dst_tag_metas)

    dst_project = create_project(dst_project_meta)
    g.dst_project_info = dst_project

    for ds_info in g.api.dataset.get_list(g.project_id):
        dst_dataset = g.api.dataset.create(dst_project.id, ds_info.name)
        if dst_project.type == str(sly.ProjectType.IMAGES):
            img_infos_all = g.api.image.get_list(ds_info.id)
            for img_infos in sly.batched(img_infos_all):
                img_names, img_ids = zip(*((x.name, x.id) for x in img_infos))
                ann_infos = g.api.annotation.download_batch(ds_info.id, img_ids)
                updated_anns = [
                    convert_image_annotation(
                        sly.Annotation.from_json(ann_info.annotation, g.project_meta),
                        config,
                        dst_tag_metas,
                    )
                    for ann_info in ann_infos
                ]
                new_img_infos = g.api.image.upload_ids(
                    dst_dataset.id, img_names, img_ids
                )
                new_img_ids = [x.id for x in new_img_infos]
                g.api.annotation.upload_anns(new_img_ids, updated_anns)
                yield len(img_infos)
        else:
            video_infos = g.api.video.get_list(ds_info.id)
            for video_info in video_infos:
                video_annotation = sly.VideoAnnotation.from_json(
                    g.api.video.annotation.download(video_info.id),
                    g.project_meta,
                    g.key_id_map,
                )
                updated_annotation = convert_video_annotation(
                    video_annotation, config, dst_tag_metas
                )
                updated_video_info = g.api.video.add_existing(
                    dst_dataset.id, video_info, name=video_info.name
                )
                g.api.video.annotation.append(updated_video_info.id, updated_annotation)
                yield 1
