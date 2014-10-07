# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

from ..extensions import db
from ..decorators import admin_required

from loctube.admin.forms import  LinkedinForm
from loctube.admin.models import  Linkedin
import requests
import json
from flask import jsonify


from pyquery import PyQuery



admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html', active='index')



@admin.route('/linkedin', methods=['GET', 'POST'])
@login_required
@admin_required
def linkedin():
    form = LinkedinForm()
    error = None
    if request.method == 'GET':
        return render_template( "admin/linkedin.html", form=form, active='linkedin')

    
    if request.method == 'POST':

        company_name = form.company.data.split('\r\n')

        error_message = ""

        try:

            json_url_part1= "https://api.linkedin.com/v1/people-search:(people:(id,public-profile-url,educations),num-results)?company-name=" + company_name[0]
                        
            access_token = "AQWV-lw8aOidUpqz9J6e09qrByd4MGBi6qgODh2fIMe1jlY_5yUFCR3SsseWjvhRMlJDwC8XmBcVvHIa22KW1lzkY7e-LaVu1aeVBHr8fXeU56Cjn7APw8h_FRrVWR4WBDizGbXPowOCByUTBC6w_taqeKMxsPC-OnKzSSzH3QA-nkbB4bo"             
            
            json_url_part2 = json_url_part1+ "&count=20&format=json&oauth2_access_token="+access_token
            
            linkedin_json = requests.get(json_url_part2)
            # Convert it to a Python dictionary
            linkedin_data = json.loads(linkedin_json.text)

            numResults = int(linkedin_data["numResults"])
            loopTo = (numResults / 20)

            if (numResults % 20) > 0: 
                loopTo +=1

            
            for i in range(0,loopTo):
            
                data = None 
                if i == 0: 
                         
                    data = linkedin_data
                else:                   
                   
                    json_url_part2 = json_url_part1 + "&start="+ str(i*20)+"&count=20&format=json&oauth2_access_token="+access_token
                    linkedin_json = requests.get(json_url_part2)
                    linkedin_data = json.loads(linkedin_json.text)
                    data = linkedin_data

                for item in data['people']['values']:

                    if item['id'] == "private": continue

                    public_pro_url = item['publicProfileUrl']

                    linkedin = Linkedin()

                    
                    public_html =PyQuery(public_pro_url); 


                    linkedin.name      = public_html(".given-name").text() + " " + public_html(".family-name").text()
                    linkedin.heading   = public_html(".headline-title.title").text()
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

                
                    db.session.add(linkedin)
                    db.session.commit()

        except Exception as inst:
            error_message += str(inst) + " - "
            pass


        flash('people has been crawled. Exception'+error_message  , 'success')

        return render_template( "admin/linkedin.html",form=form, active='linkedin')
