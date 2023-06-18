from app import app
from flask import render_template, redirect, request, session
from app.models import user_model, sighting_model





# --------------------------------------CREATE------------------------------------



@app.route('/sighting/new')
def new_sighting_form():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    return render_template('create.html', one_user = user_model.User.get_user_by_id(user_data))





@app.route('/sighting/new/create', methods = ['POST'])
def create_sighting():
    if 'user_id' not in session:
        return redirect('/')
    print(request.form)
    data = {
        'user_id': session['user_id'],
        'bid_status': request.form['bid_status'],
        'additional_notes': request.form['additional_notes'],
        'submission_date': request.form['submission_date'],
        'bid_amount': request.form['bid_amount']
    }
    print('-----------------------' , data)

    if not sighting_model.Sighting.save_sighting(data):
        return redirect ('/sighting/new')
    return redirect('/sighting/home')







# --------------------------------------READ------------------------------------


@app.route('/sighting/home')
def view_all_sightings():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    all_sightings = sighting_model.Sighting.get_all_sightings()
    print('---------------------', len(all_sightings))
    return render_template('dashboard.html', current_user=user_model.User.get_user_by_id(user_data), all_sightings = all_sightings)




@app.route('/sighting/<int:id>')
def view_one_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    id_data = {
        'id' : id
    }
    return render_template('view.html',  one_bid_proposal = sighting_model.Sighting.get_one_sighting_with_user(id_data))









# -----------------------------UPDATE---------------------------------



@app.route('/sighting/edit/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect ('/')
    sighting_data = sighting_model.Sighting.get_one_sighting_with_user({'id':id})
    return render_template('update.html', sighting_data = sighting_data)




@app.route('/sighting/update/<int:id>', methods = ['POST'])
def update_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    sighting_data = {
        'id': id,
        'user_id': session['user_id'],
        'bid_status': request.form['bid_status'],
        'additional_notes': request.form['additional_notes'],
        'submission_date': request.form['submission_date'],
        'bid_amount': request.form['bid_amount']
    }
    if not sighting_model.Sighting.validate_sighting(sighting_data):
        sighting_data = sighting_model.Sighting.get_one_sighting_with_user({'id':id})
        return render_template('update.html', sighting_data = sighting_data)
    sighting_model.Sighting.update_sighting(sighting_data)
    return redirect('/sighting/home')







# --------------------------------------------------DELETE---------------------------------------------




@app.route('/delete/<int:id>', methods=['POST'])
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/')
    sighting_data = {
        'id': id,
        'user_id': session['user_id']
    }
    sighting_model.Sighting.delete_sighting(sighting_data)
    return redirect('/sighting/home')

