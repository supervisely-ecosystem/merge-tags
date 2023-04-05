import os
from dotenv import load_dotenv

from supervisely import Api, env
import supervisely as sly


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = Api()

task_id = env.task_id()
workspace_id = env.workspace_id()
project_id = env.project_id()
project_info = api.project.get_info_by_id(project_id)
project_meta_json = api.project.get_meta(project_id)
project_meta = sly.ProjectMeta.from_json(project_meta_json)
tag_metas = project_meta.tag_metas

dst_project_info = None

key_id_map = sly.KeyIdMap()
