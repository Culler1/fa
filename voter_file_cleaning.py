import pandas as pd
import numpy as np
import glob
import os
date = '20211004'
os.mkdir('revamped_election_maps')
town_dict=pd.read_csv("voter_town_dict1.csv")
path=r'Statewide/'
all_files = glob.glob(path+"* Zone Types "+date+".txt")
zone_types=[]
for file in all_files:
    df = pd.read_table(file, header=None)
    #df.columns=df.rename(columns={0:'county',1:'col_num',2:'abbr',3:'full_name'})
    zone_types.append(df)
zone_types=pd.concat(zone_types,sort=False)
zone_types.rename(columns={0:'county',1:'col_num',2:'abbr',3:'new_name'},inplace=True)
zone_types['e_column']="district_"+zone_types.col_num.astype(str)
zone_types['new_name']=zone_types.new_name.str.lower().str.replace("municipal$",'municipality',regex=True).str.replace("u.s.",'us',regex=False).str.lower()
zone_types.drop(columns={'col_num','abbr'},inplace=True)

columndict=pd.read_csv("forcolumnheaders - Sheet1.csv")
columndict.columns=columndict.columns.str.replace(" ",'_').str.lower()
columndict['field_description']=columndict.field_description.str.replace(" ","_").str.lower()
electionmappingfiles = glob.glob(path +"*Election Map "+date+".txt")
electionmapcols=[]
for file in electionmappingfiles:
    df = pd.read_table(file, header=None)
    df.rename(columns={0:'county',1:'election_num',2:'election1',3:'date'},inplace=True)
    df['election1']=df.election1.str.lower()
    df['date']=pd.to_datetime(df.date)
    conditions = [(df['election1'].str.contains("special")),(df['election1'].str.contains("(11/8/2010)",regex=False)),
    (df['date'].dt.year!=2020)&(df['date'].dt.year % 2==1)&(df['date'].dt.month==5),
    (df['date'].dt.year!=2020)&(df['date'].dt.year % 2==0)&(df['date'].dt.month==5),
    (df['date'].dt.year % 2==1)&(df['date'].dt.month==11),
    (df['date'].dt.year % 2==0)&(df['date'].dt.month==11),
    (df['date'].dt.year==2020)&(df['date'].dt.month==6),
    (df['date'].dt.year==2004)&(df['date'].dt.month==4),
    (df['date'].dt.year==2016)&(df['date'].dt.month==4),
    (df['date'].dt.year==2008)&(df['date'].dt.month==4),
    (df['date'].dt.year==2012)&(df['date'].dt.month==4)]
    values = ['special_event','ignoreme','muni_prim',"gen_prim","muni_elect",'gen_elect','gen_prim','gen_prim','gen_prim','gen_prim','gen_prim',]
    df['election_type']=np.select(conditions,values)
    df['election_method']=df.election_type+"_"+df.date.dt.year.astype(str)+"_vote_method"
    df['election_party']=df.election_type+"_"+df.date.dt.year.astype(str)+"_party"
    df['columnparty']="election_"+df.election_num.astype(str)+'_party'
    df['columnmethod']="election_"+df.election_num.astype(str)+'_vote_method'    #df= df[['columnparty','columnmethod','election_method','election_party','county']]
    #df.columns=df.rename(columns={0:'county',1:'col_num',2:'abbr',3:'full_name'})
    electionmapcols.append(df)
electionmapcols=pd.concat(electionmapcols,sort=False)
el1=electionmapcols[['county','columnparty','election_party']]
el1.rename(columns={'columnparty':"e_column",'election_party':'new_name'},inplace=True)
el2=electionmapcols[['county','columnmethod','election_method']]
el2.rename(columns={'columnmethod':"e_column",'election_method':'new_name'}, inplace=True)
electionmapcols=pd.concat([el1,el2])
col_dict2=pd.concat([electionmapcols,zone_types])


all_files = glob.glob(path+"*Zone Codes "+date+".txt")
zone_codes=[]
for file in all_files:
    df = pd.read_table(file, header=None)
    zone_codes.append(df)

zone_codes=pd.concat(zone_codes,sort=False)
zone_codes.rename(columns={0:"county",1:"code1",2:"code2",3:"new_name"},inplace=True)


revamped_files= glob.glob(path+"* FVE "+date+".txt")
revamped_voters=[]
for file in revamped_files:
    df = pd.read_table(file, header=None)
    countyname=df.iloc[1,151]
    df.columns = df.columns+1
    df2=df[[152]]
    keys=(zone_codes[zone_codes.county.isin(df[152])].code2)
    values=(zone_codes[zone_codes.county.isin(df[152])].new_name)
    codedict=dict(zip(keys,values))
    col_dict2=pd.concat([electionmapcols,zone_types])
    col_dict2=col_dict2[col_dict2.county==df.iloc[1,151]]
    col_dict2.drop(columns={'county'},inplace=True)
    coldict3=pd.merge(columndict,col_dict2,left_on='field_description',right_on='e_column',how='left')
    coldict3['new_name'] = coldict3.new_name.fillna(coldict3.field_description)
    keys = (coldict3.field_number)
    values = (coldict3.new_name)
    coldict4 = dict(zip(keys,values))
    df.columns = df.columns.map(coldict4).str.lower()
    df['municipality']=df.municipality.map(codedict)
    df['county_1']=countyname
    keys=(town_dict[town_dict.county.isin(df.county_1)].municipality)
    values=(town_dict[town_dict.county.isin(df.county_1)].correctname)
    town_dict1=dict(zip(keys,values))
    df['municipality']=df.municipality.map(town_dict1)
    df.columns=df.columns.str.strip().str.replace(" ","_")
    #df.rename(columns={'county.1':'county_1'},inplace=True)
    df.to_csv('revamped_election_maps/'+countyname+"_revamped.csv",index=None)
