# Adding a new datadescriptor

 
Lets take an example to illustrate the procedure : 
we will add the **activity** datadescriptor

## 1. Define the Linkml model 

the linkml model permits to automate differents things that are usefull to deal with the controled vocabulary: 

* generate jsonschema model, generate pydantic model. Depends on what you prefer
* generate jsonld 
* validation of terms 


### get actual Universe repository

```
git clone https://github.com/ESPRI-Mod/WGCM_CVs.git
```

### swith to a new branch 

```
git checkout -b newDD
```


## 1. Define the linkml model 

the linkml models are in the directory "src/wgcm_cvs/schemas". we can look at one similar datadescriptor in order to create the new one. There 3 distincts methods to define the CVs : 

* list of valid terms
* a regex to valid a term 
* a composite that can be a composition of the previous one.

### Copy existing similar data descriptor

in our example **activity**. This a list of valid term.  **institution.yaml** is also a list of term. this will be our starting point. Lets copy the latter as **activity.yaml**.

### Changes according to our new data descriptor

* id : change the id and the name accordindly
* the prefixes used by the web semantic part of the service is pretty defined. just change the **institution** in **activity** in the key and the value : 
```
activity:  http://es-vocab.ipsl.fr/activity/

```
* change the default prefix to freshly created :
```
default_prefix: activity

```
* the model classes : 
Fist thing fist lets name our class like the datadesciptor with a upper first letter.
```
classes:
    Activity:

```
lets add a *description* : what is an activty ? 

```
description :an 'activity' refers to a coordinated set of modeling experiments designed to address specific scientific questions or objectives. Each activity is focused on different aspects of climate science and utilizes various models to study a wide range of climate phenomena. Activities are often organized around key research themes and may involve multiple experiments, scenarios, and model configurations.
```

*class_uri* is used to define the appropriate type in the context of web semantic : lets use our prefix and datadescriptor name : 

```
class_uri: esvocab:activity

```
the main course: the attibutes.

the basic one :


* change the slot_uri 
* validation_method doesn't have to change since we have started from a descriptor that have the same validation method . here a **list of terms**



here we have to define the model (i.e keys) for our datadescriptor :
**activity** is defined with a standard *acronym* and a *long name. We just have to keep **name** thats will be the same as **cmip_acronym** and create a **long_name**. In the new CMIP6Plus CV, there is also an url to document the activity. Lets add a **url** attribute to our model    
 


```
ttributes:
            id:
                slot_uri: activity:id
                range: string
                required: true
                identifier: true

            validation_method :
                required: true
                range : string
                ifabsent: string(list)
                slot_uri: es-vocab:validation_method

            name:
                range: string
                required: true
            
            long_name:
                range: string
                required: true
            
            cmip_acronym:
                range: string
                required: true

            url:
                range : string
                required: false
```


the linkml model is defined. This will be used by the repository to validate the defined standard terms.

## 2. Define terms

As a starting point for **activity** terms.
we will use the known activities from CMIP6 and CMIP6Plus : 

for CMIP6 : 

```
"activity_id":{
        "AerChemMIP":"Aerosols and Chemistry Model Intercomparison Project",
        "C4MIP":"Coupled Climate Carbon Cycle Model Intercomparison Project",
        "CDRMIP":"Carbon Dioxide Removal Model Intercomparison Project",
        "CFMIP":"Cloud Feedback Model Intercomparison Project",
        "CMIP":"CMIP DECK: 1pctCO2, abrupt4xCO2, amip, esm-piControl, esm-historical, historical, and piControl experiments",
        "CORDEX":"Coordinated Regional Climate Downscaling Experiment",
        "DAMIP":"Detection and Attribution Model Intercomparison Project",
        "DCPP":"Decadal Climate Prediction Project",
        "DynVarMIP":"Dynamics and Variability Model Intercomparison Project",
        "FAFMIP":"Flux-Anomaly-Forced Model Intercomparison Project",
        "GMMIP":"Global Monsoons Model Intercomparison Project",
        "GeoMIP":"Geoengineering Model Intercomparison Project",
        "HighResMIP":"High-Resolution Model Intercomparison Project",
        "ISMIP6":"Ice Sheet Model Intercomparison Project for CMIP6",
        "LS3MIP":"Land Surface, Snow and Soil Moisture",
        "LUMIP":"Land-Use Model Intercomparison Project",
        "OMIP":"Ocean Model Intercomparison Project",
        "PAMIP":"Polar Amplification Model Intercomparison Project",
        "PMIP":"Palaeoclimate Modelling Intercomparison Project",
        "RFMIP":"Radiative Forcing Model Intercomparison Project",
        "SIMIP":"Sea Ice Model Intercomparison Project",
        "ScenarioMIP":"Scenario Model Intercomparison Project",
        "VIACSAB":"Vulnerability, Impacts, Adaptation and Climate Services Advisory Board",
        "VolMIP":"Volcanic Forcings Model Intercomparison Project"
    },
```

for CMIP6Plus : 

```
"CMIP": {
            "URL": "https://gmd.copernicus.org/articles/9/1937/2016/gmd-9-1937-2016.pdf",
            "long_name": "CMIP DECK: 1pctCO2, abrupt4xCO2, amip, esm-piControl, esm-historical, historical, and piControl experiments"
        },
        "LESFMIP": {
            "URL": "https://www.frontiersin.org/articles/10.3389/fclim.2022.955414/full",
            "long_name": "The Large Ensemble Single Forcing Model Intercomparison Project"
        }
```

in the directory "data_decriptor" : create a **activity/terms** directories. Inside one term is define in one json file.

We will use a python script to create those. a little script to do that is stored in "script/DD_specific/create_activity.py". 
Eventually terms a created : an example : 
**pmip.json**

```
{
    "id": "pmip",
    "cmip_acronym": "PMIP",
    "long_name": "Palaeoclimate Modelling Intercomparison Project",
    "url": null
}
```

## 3. Here Magic happen

### Push changes

```
git commit -am "create activity datadescriptor and terms"
git push --set-upstream origin activityDD

```

### validation


then in github interface on [WGCM_CVs repository](https://github.com/ESPRI-Mod/WGCM_CVs)

#### CI/CD : Validation 

You have to wait for CI/CD to test that everything is good, if not the merge will be **cancel** ! 

what does the CI/CD : 

* create pydantic and jsonscheme model in "datadescriptors/activity/models"
* create the jsonld file version of each terms in "datadesciptors/activity/terms"
* validate the terms with the models.

validation CI/CD can be view in **Action** tab.

#### for instance with this procedure : 

the validate failed because there was a type in the linkml file name ! 

the validate failed cause of pydantic model why ? here the problem need to be tested in local. 
we can run the model creation and validate script : 

```
pdm run python scripts/generate_models.py
```
the models are stored next to terms, i cant see problem with the model. lets try to validate locally 

```
pdm run python scripts/validate.py
```
it validates everythings through json schema but not pydantic : 

```
Field required [type=missing, input_value={'id': 'aerchemmip', 'cmi...n Project', 'url': None}, input_type=dict]
```
there is a missing field, after investigation : the python script that create the terms does not include **name** attribute. Lets repair that !

```
pdm run python scripts/validate.py
```
YES !, validation is OK !
lets push changes to the origin repository

### Create a pull request 

if validation step went well, create a pull request. This will be merged into main asap. 

### The magic 

github repository is configured to send a message to the CV Service. It will be update automaticaly !!! 

## Define projects collection

Each project does not necesseraly use or even valid all the terms in the univers data descriptor. collections of valid id have to be define in each project : 

for instance, we will add activity collection id for CMIP6Plus_CVs : 

### clone the repo

```
git clone https://github.com/ESPRI-Mod/CMIP6Plus_CVs.git
```

### create a new branch

```
git checkout -b activity
```

### create collection

in directory collections :
Lets start from the institution.json and copy it as activity.json

```
{
"@context":{ 
    "@base": "http://es-vocab.ipsl.fr/Institution"
	},
"@graph":[
  {"@id":"ipsl",
   "@type":"institution",
   "name" : "Institut Pierre-Simon Laplace modified", 
   "location":{
       "city":"Paris5"
	    },
    "myprop":"42"
  },
  {
    "@id":"llnl",
    "@type":"institution"}
	]
}
```

this one is a show case to view the possibility to change metadata from universe or even add a new key in the metadata. The CV_service takes into account this specifity ! 


so for the activity, we can use the terms in universe as it. 

* change the context : just change the end of the "base" into the data descriptor name :

```
"@base": "http://es-vocab.ipsl.fr/Activity"
	}
```

* in the graph, add the list of id from universe that we need for CMIP6Plus. For now there are only 2 ( CMIP, LESFMIP). We will do it by hand. 

```
{
"@context":{ 
    "@base": "http://es-vocab.ipsl.fr/Activity"
	},
"@graph":[
  {"@id":"cmip",
   "@type":"activity"
     },
  {
    "@id":"lesmip",
    "@type":"activity"}
	]
}
```

### push change

```
git add .
git commmit -m "add activity collection"
git push --set upstream origin activity
```

and create pull request in github interface that will be done asap.

### let Magic happen 

the github CI/CD will inform the CV service to restart. 


### Test it

to test the cv service is up to date, we will use a simple curl to the API. documentation about the api is here : [http://es-vocab.ipsl.fr/docs](http://es-vocab.ipsl.fr/docs)  

```

curl -X 'GET' \                                                             
  'http://es-vocab.ipsl.fr/api/project/CMIP6Plus_CVs/collection/activity/term' \
  -H 'accept: application/json'
```

2 problems : 
* activity in CMIP6 in fact **activity_id**. Just change the name of the collection file. It will still select id from the **activity** data descriptor in WGCM_CVs

* there is not lesmip, it is a type during the procedure. it is lesfmip. Change the id inside the collection

```
curl -X 'GET' \                                                             
  'http://es-vocab.ipsl.fr/api/project/CMIP6Plus_CVs/collection/activity_id/term' \
  -H 'accept: application/json'
```
result : 

["cmip","lesfmip"] 

Perfect ! 

