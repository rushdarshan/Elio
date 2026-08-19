from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict

class InputRecord(BaseModel):
    mpn: str
    raw_text: str
    raw_manufacturer: str
    mfg_part_num: Optional[str] = None
    part_desc: Optional[str] = None
    e1_brand: Optional[str] = None
    unilog_brand: Optional[str] = None
    dib_brand: Optional[str] = None
    part_manuf: Optional[str] = None

class Brand(BaseModel):
    id: str
    label: str
    parent: Optional[str] = None

class Manufacturer(BaseModel):
    id: str
    label: Optional[str] = None
    mfr_url: Optional[str] = None

class Identity(BaseModel):
    brand: Brand
    manufacturer: Manufacturer

class Classpath(BaseModel):
    dept: str
    class_: str = Field(..., alias="class")
    fine: str
    candidate_ids: List[str] = Field(default_factory=list)

    class Config:
        populate_by_name = True

class SourceProvenance(BaseModel):
    url: str
    page: Optional[int] = None
    char_span: Optional[List[int]] = None
    snippet: str

class AttributeRecord(BaseModel):
    label: str
    value: str
    uom: str
    source: SourceProvenance
    confidence: float
    verification: str = "not_found"  # supported | contradicted | not_found

class DescriptionDetail(BaseModel):
    text: str
    chars: int
    valid: bool

class Descriptions(BaseModel):
    mobile: DescriptionDetail
    invoice: DescriptionDetail
    short: DescriptionDetail
    long: DescriptionDetail
    retail: DescriptionDetail
    marketing: DescriptionDetail

class QualityDecision(BaseModel):
    decision: str = "auto_accept"  # auto_accept | review | reject
    field_error_budget: float = 0.02
    review_reasons: List[str] = Field(default_factory=list)

class CostDetail(BaseModel):
    llm_calls: int = 0
    estimated_usd: float = 0.0

class EnrichedRecord(BaseModel):
    input: InputRecord
    identity: Identity
    classpath: Classpath
    attributes: List[AttributeRecord] = Field(default_factory=list)
    descriptions: Descriptions
    quality: QualityDecision
    cost: CostDetail
