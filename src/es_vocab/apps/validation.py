
from typing import Any
from annotated_types import doc
from fastapi import APIRouter
import es_vocab.db.cvs as cvs
import re

router = APIRouter(prefix="/app/valid")
    

def is_datadescriptor_exist(datadescriptor_id:str) -> bool:
    
    
    # the idea of decoupled test is to be able to do fuzzy search to return message like 'did you mean something ?' 
    if datadescriptor_id in list(cvs.TERMS_OF_UNIVERSE.keys()):
        return True
    ## fuzzy loukout will be here
    return False

def is_datadescriptor_term_exist(datadescriptor_id:str, term_id:str) -> bool:

    # same idea as above
    if datadescriptor_id in list(cvs.TERMS_OF_UNIVERSE.keys()):
        if term_id in list(cvs.TERMS_OF_UNIVERSE[datadescriptor_id].keys()):
            return True
    return False


def is_valid(input_term_id:str, term:Any)-> bool:
# Any cause Pydantic model could be any of each datadescriptor
    # the simple case => validation_method = "list"
    if term.validation_method=="list":
        if term.id==input_term_id:
            return True
    # the regex option
    if term.validation_method=="regex":
        match = re.match(term.regex,input_term_id)
        if match is not None:
            return True
    # the complex one => recursive composite 
    if term.validation_method=="composite":
        #print("start")
        # first split thanks to the separator if not ""
        input_parts=[] 
        if term.separator != "" :
            input_parts = input_term_id.split(term.separator)
            #print("coucou")
            if len(input_parts) != len(term.parts):
                ## TODO doesnt work if there is one or more is-required=false in parts of the composite =>> good enough for now, all parts of all composites are required 
                return False

        else:
            pass # TODO have to consider when separator ="" like in variant_label => for now .. doesnt work
        
        for i, part in enumerate(term.parts):
            dd,t = get_datadescriptor_term_from_short_uri(part.id)
            #print(dd,t)
            found_corresponding = False
            if t is None: # every term in this universe dd could be use
                for key,item in cvs.TERMS_OF_UNIVERSE[dd].items():
                    if is_valid(input_parts[i],item):
                        print("term found in dd :", input_parts[i], key)
                        found_corresponding = True
               
                if found_corresponding is not False:
                    continue

            if found_corresponding is False :
                print("not found in",dd)
                return False
            
            if t is not None: # only one term is possible inside this part of this composite
                pass # TODO implement this case 
        return True
    return False

def get_datadescriptor_term_from_short_uri(short_uri:str):
    # short_uri like : "forcing_index:one_digit"
    # return unpacked dd and term with None for term if not present
    return (short_uri.split(":")+[None])[:2] 



@router.get("{input_term_id}")
def is_valid_on_all(input_term_id:str):
    # depends on validation_method (recursive) => need function 
    res =  {}
    res["valid"] = False
    res["valid_term"] = None
    res["found_multiple"] = False
    res["multiple_match_terms"] = []
    for dd in list(cvs.TERMS_OF_UNIVERSE.keys()):
        print("trying to fing it in :",dd)
        for k,t in cvs.TERMS_OF_UNIVERSE[dd].items():
            
            if is_valid(input_term_id,t):
                if res["valid"]:
                    res["found_multiple"]=True
                    res["multiple_match_terms"].append(t)
                else:

                    res["valid term"]=t
                    res["valid"]=True
            
    return res   
