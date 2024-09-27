from pydantic import BaseModel, ConfigDict

from wgcm_cv_project_metadata.drs import DrsSpecification

class ProjectSpecs(BaseModel):
    project_id: str
    description: str
    drs_specs: list[DrsSpecification]
    model_config = ConfigDict(extra = "allow")
                              