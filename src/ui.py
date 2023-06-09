from supervisely.app.widgets import (
    Container,
    Card,
    ProjectThumbnail,
    Text,
    Button,
    Flexbox,
    Select,
    Progress,
)
import src.globals as g
import src.merge_tags as mt
import supervisely as sly


VALUE_TYPE_NAMES = {
    sly.TagValueType.NONE: "None",
    sly.TagValueType.ANY_STRING: "Any String",
    sly.TagValueType.ANY_NUMBER: "Any Number",
    sly.TagValueType.ONEOF_STRING: "One of String",
}

APPLICABLE_TO_NAMES = {
    sly.TagApplicableTo.ALL: "Videos and objects"
    if g.project_info.type == str(sly.ProjectType.VIDEOS)
    else "Images and objects",
    sly.TagApplicableTo.IMAGES_ONLY: "Videos only"
    if g.project_info.type == str(sly.ProjectType.VIDEOS)
    else "Images only",
    sly.TagApplicableTo.OBJECTS_ONLY: "Objects only",
}

selects = {}
selects_values = {}
selects_items = {}

@sly.timeit
def disable_items(name):
    for select_name, items in selects_items.items():
        disable_idxs = [i for i, item in enumerate(items) if item.value == name]
        for i in disable_idxs:
            selects[select_name].disable_item(i)

@sly.timeit
def enable_items(name):
    for select_name, items in selects_items.items():
        enable_idxs = [i for i, item in enumerate(items) if item.value == name]
        for i in enable_idxs:
            selects[select_name].enable_item(i)

def get_select(tag_meta):
    items = [
        Select.Item(tm.name, tm.name)
        for tm in g.tag_metas
        if tm.name != tag_meta.name and tm.value_type == tag_meta.value_type
    ]
    select = Select(items=items, multiple=True)

    selects_items[tag_meta.name] = items
    selects_values[tag_meta.name] = set()
    
    @select.value_changed
    @sly.timeit
    def select_value_changed(values):
        if type(values) is not list:
            return      
        
        values_set = set(values)
        
        to_disable = []
        to_enable = []
        for name in values:
            if name not in selects_values[tag_meta.name]:
                to_disable.append(name)
        for name in selects_values[tag_meta.name]:
            if name not in values_set:
                to_enable.append(name)
        for name in to_disable:
            selects[name].disable()
            disable_items(name)
        for name in to_enable:
            selects[name].enable()
            enable_items(name)
        
        if len(values_set) > 0:
            disable_items(tag_meta.name)
        else:
            enable_items(tag_meta.name)
        
        for i in range(len(items)):
            select.enable_item(i)

        selects_values[tag_meta.name] = values_set
        select.set_value(list(values_set))

    return select

def get_row(tag_meta):
    possible_values = tag_meta.possible_values
    if possible_values is None:
        possible_values = []
    hex_color = "#{:02x}{:02x}{:02x}".format(
        tag_meta.color[0], tag_meta.color[1], tag_meta.color[2]
    )
    selects[tag_meta.name] = get_select(tag_meta)
    return Container(
        widgets=[
            Text(
                f'<div style="display: flex; flex-direction: column;"> \
                    <h4 style="margin: 0 0 5px;">{tag_meta.name}</h4> \
                    <div style="display: flex; flex-wrap: wrap;">'
                + "".join(
                    f'<div class="keyword" style="font-size: x-small;">{option}</div>'
                    for option in possible_values
                )
                + "</div> \
                </div>"
            ),
            Text(APPLICABLE_TO_NAMES[tag_meta.applicable_to]),
            Text(VALUE_TYPE_NAMES[tag_meta.value_type]),
            Text(
                f'<i class="zmdi zmdi-circle ml5 mr5" style="color: {hex_color}"></i>{hex_color}'
            ),
            selects[tag_meta.name],
        ],
        direction="horizontal",
        gap=0,
        fractions=[3, 1, 1, 1, 2],
    )


input_card = Card(title="Input", content=ProjectThumbnail(g.project_info))
run_button = Button("Run", icon="zmdi zmdi-play")
progress = Progress()
progress.hide()
result_thumbnail = ProjectThumbnail()
result_thumbnail.hide()
output_card = Card(
    title="Output", content=Container(widgets=[run_button, progress, result_thumbnail])
)
input_output_cards = Flexbox(widgets=[input_card, output_card])

config_table_columns = [
    "Title",
    "Applicable to",
    "Tag value type",
    "Color",
    "Merge with",
]
config_table_header = Container(
    widgets=[
        Text(f'<span style="color: #20a0ff">{column}</span>')
        for column in config_table_columns
    ],
    gap=0,
    direction="horizontal",
    fractions=[3, 1, 1, 1, 2],
)
config_table_rows = Container(
    widgets=[get_row(tag_meta) for tag_meta in g.tag_metas], gap=20
)
config_table = Container(widgets=[config_table_header, config_table_rows], gap=25)
config_card = Card(
    title="Merge tags",
    content=config_table,
    description="Select tags to merge. Selected tags will be merged into title tag. "
    'If Tag value type is "One of String", then tag possible values will be '
    "union of merged tags. If there are two merging tags with same name and "
    "different values, two tags with same name will be created.",
)

layout = Container(widgets=[input_output_cards, config_card])

app = sly.Application(layout)


def get_config():
    conf = {}
    for tag_meta in g.tag_metas:
        conf[tag_meta.name] = selects[tag_meta.name].get_value()
    return conf


@run_button.click
def run():
    config = get_config()
    with progress(total=g.project_info.items_count) as pbar:
        run_button.hide()
        progress.show()
        for i in mt.run(config):
            pbar.update(i)
        progress.hide()
        g.dst_project_info = g.api.project.get_info_by_id(g.dst_project_info.id)
        result_thumbnail.set(g.dst_project_info)
        result_thumbnail.show()

    if sly.is_production():
        g.api.task.set_output_project(
            g.task_id, g.dst_project_info.id, g.dst_project_info.name
        )
    
    app.stop()
