from pydantic import BaseModel, Field
from typing import List, Optional

class ExamInfo(BaseModel):
    name: str = Field(description="Name of the exam")
    app_start: str = Field(description="Application start date")
    app_end: str = Field(description="Application deadline")
    exam_date: str = Field(description="Date of the exam")
    fees: str = Field(description="Application fees")

class ExamDetail(BaseModel):
    name: str
    syllabus: str
    time_to_complete: str
    resources: List[str]

class ExamState(BaseModel):
    query: str
    search_results: List[dict] = []
    extracted_exams: List[ExamInfo] = []
    top_exams: List[ExamInfo] = []
    detailed_info: List[ExamDetail] = []
    final_report: str = ""


