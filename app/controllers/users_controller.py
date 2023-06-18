from app import app
from flask import render_template, redirect, request, session, flash
from app.models.user_model import User




# --------------------------------------------CREATE---------------------------------------




@app.route('/sighting/register', methods=['POST'])
def register_user():
    file = request.files.get('profile_picture')
    data = request.form.copy() 

    if User.register(data, file):
        return redirect('/sighting/home')
    return redirect('/')




# --------------------------------------------READ---------------------------------------------



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sighting/profile')
def view_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile.')
        return redirect('/')
    
    user = User.get_user_by_id({'id': user_id})
    if not user:
        flash('User not found.')
        return redirect('/')

    return render_template('profile.html', user=user)


# ------------------------------------------------UPDATE------------------------------------
@app.route('/sighting/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_user_by_id({'id': session['user_id']})

    if request.method == 'POST':
        data = {
            'id': session['user_id'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'company_name': request.form['company_name'],
            'phone_number': request.form['phone_number']
        }

        profile_picture = request.files.get('profile_picture')

        User.update_profile(data, profile_picture)

        flash("Profile updated successfully.")
        return redirect('/sighting/profile')

    return render_template('edit_profile.html', user=user)






# ---------------------------------------------LOGIN-----------------------------------------------



@app.route('/sighting/login', methods = ['POST'])
def login_user():
    if not User.login_user(request.form):
        flash('Invalid login credentials.')
        return redirect('/')
    return redirect('/sighting/home')






# ------------------------------------------------LOGOUT---------------------------------------------




@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("You have been successfully logged out!")
    return redirect ('/')