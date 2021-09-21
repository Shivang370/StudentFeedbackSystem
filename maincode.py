import psycopg2 #convert python variable to sql variable
import requests 
from flask import Flask, render_template,request,redirect, url_for #for requesting data  like from page when data is send through post.
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import config

app = Flask(__name__)

#Create engine in postgresql for further process.
try:
    engine = create_engine('postgresql://'+config.user+':'+config.password+'@localhost:5432/'+config.database)
    #Create a pyscog connection so that python variable is converted to sql variable.
    conn = psycopg2.connect(host="localhost",database=config.database,user = config.user, password=config.password)
    cur = conn.cursor()
except:
    print("Error while creating database ")


@app.route('/',methods=["GET","POST"])
def load():
    if request.method == 'GET':
        #CHECK If request method is get render the page i.e when upload button is clicked#
        return render_template('sigin.html')
    if request.method == 'POST':
        upass = request.form.get("pass")
        print(upass)
        try:
            uid = request.form.get("id")
            print(uid)
        except ValueError:
            print("nothing found")
            return render_template("error.html",message="Invalid StudentId")
        cur.execute("select id,password from \"student\" where id = '{0}' and password = '{1}';".format(uid,upass))
        rowcount = cur.rowcount
        if rowcount > 0:
            return render_template("studenthome.html")
        else:
            return render_template("error.html",message="Wrong StudentId or password try again :)")

@app.route('/admin',methods=["GET","POST"])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')
    if request.method == 'POST':
        upass = request.form.get("pass")
        name = request.form.get("name")
        cur.execute("select name,password from \"admin\" where name = '{0}' and password = '{1}';".format(name,upass))
        rowcount = cur.rowcount
        if rowcount > 0:
            return render_template("adminhome.html")
        else:
            return render_template("error.html",message="Invalid Admin or Password :)")


#decoratar for signup.html page:
@app.route('/signup.html',methods=["POST","GET"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    if request.method == 'POST':
        uid = request.form.get("id")      #request data from the form filled on sigin.html with attribut name="id"
        uname = request.form.get("uname")
        upass = request.form.get("pass")
        ucourse = request.form.get("ucourse")
        usemester = request.form.get("semester")
        uaddress = request.form.get("uaddress")
        umobile = request.form.get("unumber")
        email = request.form.get("email")
        #cur.execute("INSERT INTO student (id,name,password,course,address,mobile,email) VALUES (:id,:name,:password,:course,:address,:mobile,:email)",{'id':uid, 'name':uname, 'password':upass, 'course':ucourse, 'address':uaddress, 'mobile':umobile, 'email':email})
        cur.execute('''INSERT INTO student (id, name,semester,scourseid,address,mobile,email,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''',  (uid,uname,usemester,ucourse,uaddress,umobile,email,upass))
        conn.commit()
    return render_template("sigin.html")

@app.route('/canteenfeedback',methods=["GET","POST"])
def canteenfeedback():
    if request.method == 'GET':
        return render_template('canteenfeedback.html')
    if request.method == 'POST':
        food_quality = request.form.get("quality_food")
        hygen = request.form.get("hygen")
        staff_service = request.form.get("staff_service")
        suggestion = request.form.get("suggestion")
        enrollmentno = request.form.get("enrollmentid")
        cur.execute('''INSERT INTO canteenfeedback (foodquality,hygen_cleanliness,staffservice_behaviour,suggestion,cstudentid) VALUES (%s,%s,%s,%s,%s)''',  (food_quality,hygen,staff_service,suggestion,enrollmentno))
        conn.commit()
        return render_template('studenthome.html')


@app.route('/academicfeedback',methods=["GET","POST"])
def academicfeedback():
    if request.method == 'GET':
        return render_template('academicfeedback.html')
    if request.method == 'POST':
        Teaching_quality = request.form.get("teaching")
        Guidance = request.form.get("guidance")
        Quality_course_content = request.form.get("course")
        Suggestion = request.form.get("suggestion")
        Subject_Interest = request.form.get("Interest")
        Semester_Experience = request.form.get("Semester_exp")
        CourseId = request.form.get("courseid")
        Semester = request.form.get("Semester")
        Subjectid = request.form.get("subjectid")
        Faculty_ID = request.form.get("FacultyID")  
        print(Teaching_quality)
        print(Guidance)
        print(CourseId)
        print(Quality_course_content)
        print(Suggestion)
        print(Subject_Interest)
        print(Semester_Experience)
        print(Semester)
        print(Faculty_ID)      
        cur.execute('''INSERT INTO academicfeedback (Teaching_quality,Guidance,Quality_course_content,Suggestion,Subject_Interest,Semester_Experience,CourseId,Faculty_ID,Subjectid ,Semester) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(Teaching_quality,Guidance,Quality_course_content,Suggestion,Subject_Interest,Semester_Experience,CourseId,Faculty_ID,Subjectid ,Semester))
        conn.commit()
        return render_template('studenthome.html')
        

@app.route('/alldata',methods=["GET","POST"])
def alldata():
    if request.method == 'GET':
        return render_template('viewmore.html')


@app.route('/sportfeedback',methods=["GET","POST"])
def sportfeedback():
    if request.method == 'GET':
        return render_template('event_sport_feedback.html')
    if request.method == 'POST':
        sport_resource = request.form.get("sport_resource")
        sport_space = request.form.get("space")
        coach_availability = request.form.get("coach__availability")
        suggestion = request.form.get("suggestion")
        dress_quality = request.form.get("dress_quality")
        sportadded = request.form.get("sportadded")
        id = request.form.get("enrollmentid")
        print(sport_resource)
        print(sport_space)
        print(coach_availability)
        print(suggestion)
        print(dress_quality)
        print(sportadded)
        cur.execute('''INSERT INTO sportfeedback (sport_resource,sport_space,coach_availability,suggestion,dress_quality,ranking_performance,sid) VALUES (%s,%s,%s,%s,%s,%s,%s)''',  (sport_resource,sport_space,coach_availability,suggestion,dress_quality,sportadded,id))
        conn.commit()
        return render_template('studenthome.html')
        


@app.route('/facultydata',methods=["GET","POST"])
def facultydata():
    cur.execute("select * from faculty") #it return none
    headervalue = ["Faculty_Id","Faculty_Name","F_Course Id","F_Subject Id","F_Dept_id","F_Email","F_Address","F_MobileNo."]
    print(headervalue)
    result = [list(r) for r in cur.fetchall()] #fetchall() fuction use to fetch all the data of database fetchone() for single row
    # Need for above line is to convert list[] to get list of tuples like this => [("1","shash"),(),()]
    # for r in result:
    #     print(r)
    conn.commit() #use to execute the query and commit it 
    return render_template("faculty.html",collen=len(headervalue),header = headervalue ,indexval = result)


@app.route('/faculty',methods=["GET","POST"])
def faculty():
    if request.method == 'GET':
        success = request.args.get('check') #tp get ajax agrument
        print(success)
        if  success == "deletevalue":
            headervalue = ["Faculty_Id","Faculty_Name","F_Course Id","F_Subject Id","F_Dept_id","F_Email","F_Address","F_MobileNo."]
            string = "select \""
            header = ["fid","fname","fcourseid","fsubjectid","fdeptid","femail","faddress","fmobile"]
            indexval = request.args.get('key')
            print(indexval)
            for a in range(len(header)):
                if a == len(header)-1:
                    string = string + header[a]+ "\" from faculty;"
                else:
                    string = string + header[a] +"\",\""
            string1 = "Delete from faculty where fsubjectid = '%s';"%(indexval)
            cur.execute(string1)
            cur.execute(string)
            result = [list(r) for r in cur.fetchall()]
            # for r in result:
            #     print(r)
            conn.commit()
            return render_template("faculty.html",collen=len(headervalue),header = headervalue ,indexval = result)
        elif success == "editval":
            print("inside editedvalue")
            editval = []
            editval.append(request.args.get('key1'))
            editval.append(request.args.get('key2'))
            editval.append(request.args.get('key3'))
            editval.append(request.args.get('key4'))
            editval.append(request.args.get('key5'))
            editval.append(request.args.get('key6'))
            editval.append(request.args.get('key7'))
            index = request.args.get('key4')
            headervalue = ["Faculty_Id","Faculty_Name","F_Course Id","F_Subject Id","F_Dept_id","F_Email","F_Address","F_MobileNo."]
            header = ["fid","fname","fcourseid","fsubjectid","fdeptid","femail","faddress","fmobile"]
            string="UPDATE faculty SET \""
            for a in range(len(header)):
                if a == len(header)-1:
                    string = string + header[a] + "\" = '" + editval[a] +"' where \"fsubjectid\" = '" + index +"';"
                else:
                    string = string + header[a] +"\" = '" + editval[a] +"',\""
            print(string)
            cur.execute(string)
            string1 = "select \""
            for a in range(len(header)):
                if a == len(header)-1:
                    string1 = string1 + header[a]+ "\" from faculty;"
                else:
                    string1 = string1 + header[a] +"\",\""
            print(string1)
            cur.execute(string1)
            result = [list(r) for r in cur.fetchall()]
            for r in result:
                print(r)
            conn.commit()
            return render_template("faculty.html",collen=len(headervalue),header = headervalue ,indexval = result)
    if request.method == 'POST':
        fname = request.form.get("Faculty_Name")
        fid = request.form.get("Faculty_Id")
        femail = request.form.get("F_Email")
        fcourseid = request.form.get("F_Course Id")
        fsubjectid = request.form.get("F_Subject Id")
        fdeptid = request.form.get("F_Dept_id")
        faddress = request.form.get("F_Address")
        fmobile = request.form.get("F_MobileNo.")
        cur.execute('''INSERT INTO faculty (fid,fname,fcourseid,fsubjectid,fdeptid,femail,faddress,fmobile) VALUES (%s,%s,%s,%s,%s,%s,%s)''',  (fid,fname,fcourseid,fsubjectid,femail,faddress,fmobile))
        conn.commit()
        return redirect(url_for('facultydata'))


@app.route('/adminstudent',methods=["GET","POST"])
def adminstudent():
    headervalue = ["StudentId","StudentName","Semester","StudentCourseID","Address","MobileNo.","Email"]
    string = "select \""
    header = ["id","name","semester","scourseid","address","mobile","email"]
    for a in range(len(header)):
        if a == len(header)-1:
            string = string + header[a]+ "\" from Student;"
        else:
            string = string + header[a] +"\",\""
    print(string)
    cur.execute(string)
    result = [list(r) for r in cur.fetchall()]
    for r in result:
        print(r)
    conn.commit()
    print(len(headervalue))
    return render_template("adminstudent.html",collen = len(headervalue), header = headervalue,indexval = result)


@app.route('/adminfacultyupdate')
def adminfacultyupdate():
    success = request.args.get('check')
    print(success)
    if  success == "deletevalue":
        headervalue = ["StudentId","StudentName","Semester","StudentCourseID","Address","MobileNo.","Email"]
        string = "select \""
        header = ["id","name","semester","scourseid","address","mobile","email"]
        indexval = request.args.get('key')
        print(indexval)
        for a in range(len(header)):
            if a == len(header)-1:
                string = string + header[a]+ "\" from Student;"
            else:
                string = string + header[a] +"\",\""
        string1 = "Delete from student where id = '%s';"%(indexval)
        cur.execute(string1)
        cur.execute(string)
        result = [list(r) for r in cur.fetchall()]
        for r in result:
            print(r)
        conn.commit()
        return render_template("adminstudent.html",collen=len(headervalue),header = headervalue ,indexval = result)
    elif success == "editval":
        print("inside editedvalue")
        editval = []
        editval.append(request.args.get('key1'))
        editval.append(request.args.get('key2'))
        editval.append(request.args.get('key3'))
        editval.append(request.args.get('key4'))
        editval.append(request.args.get('key5'))
        editval.append(request.args.get('key6'))
        editval.append(request.args.get('key7'))
        editval.append(request.args.get('key8'))
        index = request.args.get('key1')
        headervalue = ["StudentId","StudentName","Department","Semester","StudentCourse","Address","MobileNo.","Email"]
        string = "select \""
        header = ["id","name","department","semester","course","address","mobile","email"]
        string="UPDATE student SET \""
        for a in range(len(header)):
            if a == len(header)-1:
                string = string + header[a] + "\" = '" + editval[a] +"' where \"id\" = '" + index +"';"
            else:
                string = string + header[a] +"\" = '" + editval[a] +"',\""
        print(string)
        cur.execute(string)
        string1 = "select \""
        for a in range(len(header)):
            if a == len(header)-1:
                string1 = string1 + header[a]+ "\" from Student;"
            else:
                string1 = string1 + header[a] +"\",\""
        print(string1)
        cur.execute(string1)
        result = [list(r) for r in cur.fetchall()]
        for r in result:
            print(r)
        conn.commit()
        return render_template("adminstudent.html",collen=len(headervalue),header = headervalue ,indexval = result)




@app.route('/adminstudentupdate')
def adminstudentupdate():
    success = request.args.get('check')
    print(success)
    if  success == "deletevalue":
        headervalue = ["StudentId","StudentName","Semester","StudentCourseID","Address","MobileNo.","Email"]
        string = "select \""
        header = ["id","name","semester","scourseid","address","mobile","email"]
        indexval = request.args.get('key')
        print(indexval)
        for a in range(len(header)):
            if a == len(header)-1:
                string = string + header[a]+ "\" from Student;"
            else:
                string = string + header[a] +"\",\""
        string1 = "Delete from student where id = '%s';"%(indexval)
        cur.execute(string1)
        cur.execute(string)
        result = [list(r) for r in cur.fetchall()]
        for r in result:
            print(r)
        conn.commit()
        return render_template("adminstudent.html",collen=len(headervalue),header = headervalue ,indexval = result)
    elif success == "editval":
        print("inside editedvalue")
        editval = []
        editval.append(request.args.get('key1'))
        editval.append(request.args.get('key2'))
        editval.append(request.args.get('key3'))
        editval.append(request.args.get('key4'))
        editval.append(request.args.get('key5'))
        editval.append(request.args.get('key6'))
        editval.append(request.args.get('key7'))
        editval.append(request.args.get('key8'))
        index = request.args.get('key1')
        print(index)
        headervalue = ["StudentId","StudentName","Semester","StudentCourseID","Address","MobileNo.","Email"]
        header = ["id","name","semester","scourseid","address","mobile","email"]
        string="UPDATE student SET \""
        for a in range(len(header)):
            if a == len(header)-1:
                string = string + header[a] + "\" = '" + editval[a] +"' where \"id\" = '" + index +"';"
            else:
                string = string + header[a] +"\" = '" + editval[a] +"',\""
        print(string)
        cur.execute(string)
        string1 = "select \""
        for a in range(len(header)):
            if a == len(header)-1:
                string1 = string1 + header[a]+ "\" from Student;"
            else:
                string1 = string1 + header[a] +"\",\""
        print(string1)
        cur.execute(string1)
        result = [list(r) for r in cur.fetchall()]
        for r in result:
            print(r)
        conn.commit()
        return render_template("adminstudent.html",collen=len(headervalue),header = headervalue ,indexval = result)



@app.route('/viewcanteenfeedback',methods=["GET","POST"])
def viewcanteenfeedback():
    cur.execute("select * from canteenfeedback")
    headervalue = ["StudentId","Foodquality","Hygen_cleanliness","Staffservice_behaviour","Suggestion"]
    result = [list(r) for r in cur.fetchall()]
    # for r in result:
    #     print(r)
    conn.commit()
    return render_template("viewcanteenfeedback.html",collen=len(headervalue),header = headervalue ,indexval = result)

@app.route('/viewacademicfeedback',methods=["GET","POST"])
def viewacademicfeedback():
    cur.execute("select * from ACADEMICFEEDBACK")
    headervalue = ["Teaching_Quality","Guidance","Quality_course_content","Subject_Interest","Semester_Experience","Suggestion","Semester","CourseId"," Subjectid","Faculty_ID"]
    result = [list(r) for r in cur.fetchall()]
    # for r in result:
    #     print(r)
    conn.commit()
    return render_template("viewacademicfeedback.html",collen=len(headervalue),header = headervalue ,indexval = result)

@app.route('/viewsportfeedback',methods=["GET","POST"])
def viewsportfeedback():
    cur.execute("select * from sportfeedback")
    headervalue = ["StudentId","Sport_resource","Sport_space","Coach_availability","Suggestion","Dress_quality","Ranking_performance"]
    result = [list(r) for r in cur.fetchall()]
    # for r in result:
    #     print(r)
    conn.commit()
    return render_template("viewsportfeedback.html",collen=len(headervalue),header = headervalue ,indexval = result)




if __name__ == "__main__":
    app.run(debug=True)