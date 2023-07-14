from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask'
db = SQLAlchemy(app)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    agreed_terms = db.Column(db.Boolean, nullable=False)

    def authenticate(email, password):
        return Admin.query.filter_by(email=email, password=password).first()

class TeamLeader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    agreed_terms = db.Column(db.Boolean, nullable=False)
    assign_company = db.Column(db.String(255)) 

    def authenticate(email, password):
        return TeamLeader.query.filter_by(email=email, password=password).first()

class Recruiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    agreed_terms = db.Column(db.Boolean, nullable=False)
    assign_vacancy = db.Column(db.String(255)) 

    @staticmethod
    def authenticate(email, password):
        return Recruiter.query.filter_by(email=email, password=password).first()

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    phone = db.Column(db.String(20))

    vacancies = db.relationship('Vacancy', backref='company', lazy=True)

class JobApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    qualification = db.Column(db.String(255), nullable=False)
    assign_vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'))
    experience = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    reason_to_leave = db.Column(db.Text, nullable=False)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'))
    vacancy = db.relationship('Vacancy', foreign_keys=[vacancy_id])

    assigned_vacancy = db.relationship('Vacancy', backref='applicants', foreign_keys=[assign_vacancy_id])
    applied_vacancy = db.relationship('Vacancy', backref='job_app3', foreign_keys=[vacancy_id])


class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    job_applications = db.relationship('JobApp', foreign_keys=[JobApp.vacancy_id])

class CompanyDetails(db.Model):
    __tablename__ = 'place_terms'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    term1 = db.Column(db.Boolean, nullable=False)
    term2 = db.Column(db.Boolean, nullable=False)
    term3 = db.Column(db.Boolean, nullable=False)
    term4 = db.Column(db.Boolean, nullable=False)
    term5 = db.Column(db.Boolean, nullable=False)

class PostJob(db.Model):
    __tablename__ = 'post_job'
    id = db.Column(db.Integer, primary_key=True)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    num_vacancies = db.Column(db.Integer, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Numeric(10, 2), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    vacancy = db.relationship('Vacancy', backref=db.backref('jobs', lazy=True))

class AppUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_app_id = db.Column(db.Integer, db.ForeignKey('job_app.id'))
    status = db.Column(db.String(50))
    remark = db.Column(db.Text)

    def __init__(self, job_app_id, status, remark):
        self.job_app_id = job_app_id
        self.status = status
        self.remark = remark

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_signup')
def admin_signup():
    return render_template('admin_signup.html')

@app.route('/rec_login')
def rec_login():
    return render_template('rec_login.html')

@app.route('/tl_login')
def tl_login():
    return render_template('tl_login.html')

@app.route('/rec_signup')
def rec_signup():
    return render_template('rec_signup.html')

@app.route('/tl_signup')
def tl_signup():
    return render_template('tl_signup.html')

@app.route('/com_details')
def com_details():
    return render_template('com_details.html')

@app.route('/vac_details')
def vac_details():
    return redirect(url_for('add_vacancy'))


@app.route('/tl_view')
def tl_view():
    return render_template('tl_view.html')

@app.route('/rec_view')
def rec_view():
    recruiters = Recruiter.query.all()
    vacancies = Vacancy.query.all()
    return render_template('rec_view.html', vacancies=vacancies , recruiters=recruiters)

@app.route('/assign', methods=['GET', 'POST'])
def assign():
    return render_template('tl_assign.html')

@app.route('/place_terms', methods=['GET'])
def place_terms():
    companies = Company.query.all()
    return render_template('place_terms.html', companies=companies)

@app.route('/post_job', methods=['GET'])
def post_job():
    vacancies = Vacancy.query.all()
    return render_template('post_job.html', vacancies=vacancies)

@app.route('/assign2', methods=['GET', 'POST'])
def assign2():
    return render_template('rec_assign.html')

@app.route('/job_app')
def job_app():
    vacancies = Vacancy.query.all()
    return render_template('job_app.html', vacancies=vacancies)

@app.route('/app_up')
def app_up():
    job_apps = JobApp.query.all()
    return render_template('app_up.html', job_apps = job_apps)

@app.route('/app_view')
def app_view():
     vacancies = Vacancy.query.all()
     job_apps = JobApp.query.all()
     app_ups = AppUp.query.all()
     return render_template('app_view.html', vacancies = vacancies ,job_apps = job_apps , app_ups = app_ups)


@app.route('/admin', methods = ['POST'])
def admin_signup1():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['address']
    phone = request.form['phone']
    dob = request.form['dob']
    email = request.form['email']
    password = request.form['password']
    gender = request.form['gender']
    agreed_terms = bool(request.form.get('terms'))

    new_admin = Admin(
        first_name=first_name,
        last_name=last_name,
        address=address,
        phone=phone,
        dob=dob,
        email=email,
        password=password,
        gender=gender,
        agreed_terms=agreed_terms
    )

    db.session.add(new_admin)
    db.session.commit()
    db.create_all()

    return 'Admin registered successfully!'

@app.route('/teamleader/signup', methods=['POST'])
def team_leader_signup():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['address']
    phone = request.form['phone']
    dob = request.form['dob']
    email = request.form['email']
    password = request.form['password']
    gender = request.form['gender']
    agreed_terms = bool(request.form.get('terms'))
    assign_company = request.form['assign_company']

    new_team_leader = TeamLeader(
        first_name=first_name,
        last_name=last_name,
        address=address,
        phone=phone,
        dob=dob,
        email=email,
        password=password,
        gender=gender,
        agreed_terms=agreed_terms,
        assign_company=assign_company
    )

    db.session.add(new_team_leader)
    db.session.commit()
    db.create_all()

    return 'Team Leader registered successfully!'

@app.route('/recruiter/signup', methods=['POST'])
def recruiter_signup():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['address']
    phone = request.form['phone']
    dob = request.form['dob']
    email = request.form['email']
    password = request.form['password']
    gender = request.form['gender']
    agreed_terms = bool(request.form.get('terms'))
    assign_vacancy = request.form['assign_vacancy']

    new_recruiter = Recruiter(
        first_name=first_name,
        last_name=last_name,
        address=address,
        phone=phone,
        dob=dob,
        email=email,
        password=password,
        gender=gender,
        agreed_terms=agreed_terms,
        assign_vacancy=assign_vacancy
    )

    db.session.add(new_recruiter)
    db.session.commit()
    db.create_all()

    return 'Recruiter registered successfully!'

@app.route('/company/add', methods=['POST'])
def add_company():
    name = request.form['name']
    industry = request.form['industry']
    location = request.form['location']
    description = request.form['description']
    website = request.form['website']
    phone = request.form['phone']

    new_company = Company(
        name=name,
        industry=industry,
        location=location,
        description=description,
        website=website,
        phone=phone
    )
    db.session.add(new_company)
    db.session.commit()

    return 'Company Added successfully!!'


@app.route('/company/vacancy/add', methods=['GET','POST'])
def add_vacancy():
    if request.method == 'POST':
        company_id = request.form['company']
        position = request.form['position']
        location = request.form['location']
        description = request.form['description']

        new_vacancy = Vacancy(
                position=position,
                location=location,
                description=description,
                company_id=company_id
        )

        db.session.add(new_vacancy)
        db.session.commit()

        return 'Vacancies Added successfully!!'

    companies = Company.query.all()
    return render_template('vac_details.html',companies=companies)

@app.route('/admin/login', methods=['GET' , 'POST'])
def admin_login1():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Admin.authenticate(email, password)
        if user and user.password == password:
            return render_template('admin_home.html')
        else:
            return 'Invalid email or password'
    return render_template('admin_login.html')

@app.route('/teamleader/login', methods=['GET', 'POST'])
def teamleader_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = TeamLeader.authenticate(email, password)
        if user and user.password == password:
            data = TeamLeader.query.all()
            return render_template('tl_home.html', data=data)
        else:
            return 'Invalid email or password'
    return render_template('tl_login.html')

@app.route('/teamleader/tl_view')
def teamleader_view():
    print("Inside teamleader_view function")
    team_leaders = TeamLeader.query.all()
    companies = Company.query.all()
    return render_template('tl_view.html', team_leaders=team_leaders , companies=companies)

@app.route('/recruiter/login', methods=['GET', 'POST'])
def recruiter_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Recruiter.authenticate(email, password)
        if user and user.password == password:
            data = Recruiter.query.all()
            return render_template('rec_home.html', data=data)
        else:
            return 'Invalid email or password'
    return render_template('rec_login.html')

@app.route('/recruiter/rec_view')
def recruiter_view():
    print("Inside teamleader_view function")
    recruiters = Recruiter.query.all()
    vacancies = Vacancy.query.all()
    return render_template('rec_view.html', recruiters=recruiters , vacancies=vacancies)


@app.route('/tl_assign', methods=['GET', 'POST'])
def assign1():
    if request.method == 'POST':
        assign_company = request.form['assign_company']
        team_leader_id = request.form['team_leader']
        team_leader = TeamLeader.query.get(team_leader_id)
        team_leader.assign_company = assign_company
        db.session.commit()
        return 'Company assigned to Team Leader'

    team_leaders = TeamLeader.query.all()
    companies = Company.query.all()

    return render_template('tl_assign.html', team_leaders=team_leaders, companies=companies)

@app.route('/place_terms', methods=['POST'])
def place_terms1():
    company_id = request.form.get('company_id')
    term1 = bool(request.form.get('term1'))
    term2 = bool(request.form.get('term2'))
    term3 = bool(request.form.get('term3'))
    term4 = bool(request.form.get('term4'))
    term5 = bool(request.form.get('term5'))

    place_terms = CompanyDetails(company_id=company_id, term1=term1, term2=term2, term3=term3, term4=term4, term5=term5)
    db.session.add(place_terms)
    db.session.commit()

    return 'Company added placement terms !!!'

@app.route('/post_job', methods=['POST'])
def post_job1():
    if request.method == 'POST':
        vacancy_id = request.form['vacancy_id']
        vacancy = Vacancy.query.filter_by(id=vacancy_id).first()
        position = vacancy.position if vacancy else None
        num_vacancies = request.form['num_vacancies']
        requirements = request.form['requirements']
        experience = request.form['experience']
        salary = request.form['salary']
        contact_email = request.form['contact_email']

        position = position if position is not None else ''
        
        job = PostJob(
            vacancy_id=vacancy_id,
            position=position,
            num_vacancies=num_vacancies,
            requirements=requirements,
            experience=experience,
            salary=salary,
            contact_email=contact_email
        )

        db.session.add(job)
        db.session.commit()

        return 'Job posted successfully!'

    vacancies = Vacancy.query.all()

    return render_template('post_job.html', vacancies=vacancies)

@app.route('/rec_assign', methods=['GET', 'POST'])
def rec_assign1():
    if request.method == 'POST':
        assign_vacancy = request.form['assign_vacancy']
        recruiter_id = request.form['recruiter']

        recruiter = Recruiter.query.get(recruiter_id)
        recruiter.assign_vacancy = assign_vacancy

        db.session.commit()

        return 'Vacancy assigned to recruiter successfully!'

    recruiters = Recruiter.query.all()
    vacancies = Vacancy.query.all()

    return render_template('rec_assign.html', recruiters=recruiters, vacancies=vacancies)

@app.route('/job_app', methods=['GET', 'POST'])
def job_app1():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        qualification = request.form['qualification']
        assign_vacancy_id = int(request.form['assign_vacancy'])
        experience = request.form['experience']
        location = request.form['location']
        reason_to_leave = request.form['reason']

        assign_vacancy_id = int(request.form['assign_vacancy'])
        assigned_vacancy = Vacancy.query.get(assign_vacancy_id)

        new_job_app = JobApp(
            full_name=full_name,
            email=email,
            phone=phone,
            qualification=qualification,
            assign_vacancy_id=assign_vacancy_id,
            experience=experience,
            location=location,
            reason_to_leave=reason_to_leave,
            assigned_vacancy=assigned_vacancy
        )

        db.session.add(new_job_app)
        db.session.commit()

        return 'Job application submitted successfully!'
    else:
        vacancies = Vacancy.query.all()
        return render_template('job_app.html', vacancies=vacancies)

@app.route('/app_up', methods=['GET', 'POST'])
def app_up1():
    if request.method == 'POST':
        job_app_id = request.form['select_applicant']
        status = request.form['status']
        remark = request.form['remark']

        new_app_up = AppUp(job_app_id=job_app_id, status=status, remark=remark)
        db.session.add(new_app_up)
        db.session.commit()

        return 'Application updated successfully!'

    else:
        job_apps = JobApp.query.all()  # Assuming JobApp is the model for the job_app table
        return render_template('app_up.html', job_apps=job_apps)

if __name__ == '__main__':
    app.run()
