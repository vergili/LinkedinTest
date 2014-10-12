from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
from sys import argv
from pyquery import PyQuery
from lxml import etree
import urllib
import json

#please write your own mysql connection here
engine = create_engine('mysql://vergili1_temp:Zeynep.2008@plover.arvixe.com:3306/vergili1_deneme?charset=utf8', echo=False)


Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

#All text area defined as a TEXT of course small lengt text can be selected as a string. 
class Linkedin(Base):

    __tablename__ = 'linkedin'

    id               = Column(Integer, primary_key=True)
    name             = Column(Text(collation='utf8_general_ci')) 
    heading          = Column(Text(collation='utf8_general_ci')) 
    location         = Column(Text(collation='utf8_general_ci')) 
    summary          = Column(Text(collation='utf8_general_ci')) 
    education        = Column(Text(collation='utf8_general_ci')) 
    positions        = Column(Text(collation='utf8_general_ci'))
    
    def __repr__(self):
        return "%s, %s" % (self.name.encode('utf-8'), self.heading.encode('utf-8')) 


companyName =  raw_input('What CompanyName on Linkedin:')
print 'Complete the linkedin company page link.  Example for imatchative: imatchative-corp-  '
companyLinkExt =  raw_input('https://www.linkedin.com/company/:')

print ''
print '#########################################################################'
print '#                                                                       #'
print '#                 CRAWLING is Starting                                  #'
print '# Please Note that if there is no connection between company empoyees   #'
print '# or if employee hide his/her information like company name the crawler #'
print '# can not find that member                                              #'
print '#                                                                       #'
print '#########################################################################'
print ''

linkedin_company_url = "https://www.linkedin.com/company/"+companyLinkExt

companyHtml = PyQuery(url=linkedin_company_url);

firstLinks = companyHtml(".discovery-photo");

listOfpeople = [a.attrib['href'].split("?")[0]  for a in firstLinks];

newList =[]


oldListOfpeople = []
i = 0
j = 1
while i < len(listOfpeople):

    try:
        memberHtml = PyQuery(url=listOfpeople[i] );

        memberPublicUrl = listOfpeople[i]

        listOfpeople.remove(listOfpeople[i])

        newLinks = memberHtml(".with-photo strong a")
        if len(newLinks) == 0:
            newLinks = memberHtml(".insights-browse-map:first h4 a")

        current = memberHtml(".org.summary").text()
        if current == "" or companyName not in current.lower():
            current = memberHtml("#overview-summary-current li").text()
        elif current == "" or companyName not in current.lower():
            current = memberHtml(".summary-current li").text()

        
        past    = memberHtml(".past").text()
        if past == "" or companyName not in past.lower():
            past = memberHtml("#overview-summary-past").text()
        elif past == "" or companyName not in past.lower():
            past = memberHtml(".summary-past li").text()


        if companyName not in current.lower() and companyName not in past.lower() :  continue
    
        newList = [a.attrib['href'].split("?")[0]  for a in newLinks];

    
        yeniList = [a for a in newList if a not in listOfpeople and a not in oldListOfpeople ]
  
        oldListOfpeople.append(memberPublicUrl)
    
        listOfpeople += yeniList 

        linkedin = Linkedin()

        public_html =PyQuery(memberPublicUrl); 

        linkedin.name      = public_html(".full-name").text() 

        heading  = public_html(".headline-title.title").text()
        if heading =="": 
            heading  = public_html("#headline").text()
        linkedin.heading   = heading

        linkedin.location  = public_html(".locality").text()
        linkedin.summary   = public_html(".description.summary").text()
          

        educations_list = [] 
        for k in range(0, len(public_html(".education .summary"))):
            selector = ".education:eq(" +str(k)+ ")"
                    
            education_dict = {}

            education_dict = { "school":public_html(selector+" .summary").text(), 
                                "degree": public_html(selector+" .major").text(),
                                "dtstart": public_html(selector+" .dtstart").text(),
                                "dtend":  public_html(selector+" .dtend").text() }
                     
            educations_list.append(education_dict)

        positions_list = [] 
        for k in range(0, len(public_html(".experience .title"))):
            selector = ".experience:eq(" +str(k)+ ")" 

            position_dict = {}

            position_dict = { "title":public_html(selector+" .title").text(), 
                                "company": public_html(selector+" .org").text(),
                                "dtstart": public_html(selector+" .dtstart").text(),
                                "dtend":  public_html(selector+" .dtend").text() }
                     
            positions_list.append(position_dict)



        linkedin.education = json.dumps(educations_list)
        linkedin.positions = json.dumps(positions_list)

                
        session.add(linkedin)
        session.commit()

        print j
        j+=1
        print linkedin
        print "\n"


    except Exception as message:
        print str(message) 
        pass



