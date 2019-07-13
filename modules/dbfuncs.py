from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
   
   
def dbGetEngine(host,port,database,user,password):
    #return create_engine('postgresql+psycopg2://weukgmth:EjnV3ZckgHVsF9P8uTRO-WkmESwBTzOB@manny.db.elephantsql.com:5432/weukgmth')    
    return create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")    
    
    
def dbGetSession(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

