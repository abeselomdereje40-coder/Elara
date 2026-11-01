from dataclasses import dataclass,field
from typing import List,Dict,Optional

@dataclass
class ResearchRequest:
    query:str
    depth:str = "standard"
    goal:str =""
    requirments:List[str]=field(default_factory=list)

@dataclass
class searchResult:
    title:str
    url:str
    content:str=""
    score:float = 0.0
    domain:str=""

@dataclass
class Evidence:
    claim:str
    evidence:str
    source_url:str
    source_title:str=""
    confidence:str="unknown"
    verified:bool=False

@dataclass
class ResearchContent:
    query:str
    goal:str=""
    findings:List[Dict]=field(default_factory=list)
    verified_facts:List[Evidence]=field(default_factory=list)
    conflict:List[Dict]=field(default_factory=list)
    unverified_claim:List[Evidence]=field(default_factory=list)
    sources:List[searchResult]=field(default_factory=list)