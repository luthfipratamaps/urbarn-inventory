from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, \
    jsonify, current_app, make_response
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, EmptyForm, AddLocationForm, EditLocationForm, \
     AddProductForm, EditProductForm, AddCategoryForm, EditCategoryForm, \
     TransferProductForm
from app.models import User, Product, Location, Category, Transfer, Balance, Role
from app.main import bp
from sqlalchemy.exc import IntegrityError

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    balance = Balance.query.all()
    exists = bool(Balance.query.all())
    if exists== False :
        flash(f'Add products,locations and make transfers to view','info')
    return render_template('index.html' ,balance=balance)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.email)
    
    roles = Role.query.with_entities(Role.name).order_by(Role.id).all()
    roles_list = []
    for role in roles:
        roles_list.append(role[-1])
    form.role.choices = roles_list
    
    id = request.args.get('id')
    if form.validate_on_submit():
        this_role = Role.query.filter_by(name = form.role.data).first()
        role_id = this_role.id
        if id:
            user = User.query.filter_by(id = id).first()
            user.username = form.username.data
            user.email = form.email.data
            user.role_id = role_id
            db.session.commit()
            flash('Your changes have been saved.','success')
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.role_id = role_id
            db.session.commit()
            flash('Your changes have been saved.','success')
        return redirect(url_for('main.manage_user'))
    elif request.method == 'GET':
        if id:
            user = User.query.filter_by(id = id).first()
            form.username.data = user.username
            form.email.data = user.email
        else:
            form.username.data = current_user.username
            form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@bp.route("/manage_user", methods = ['GET', 'POST'])
@login_required
def manage_user():
    if current_user.role_id not in (1,2):
        flash(f'You don\'t have the permission','danger')
        return redirect(url_for('main.index'))
    
    details = User.query.all()
    exists = bool(User.query.all())
    if exists== False and request.method == 'GET':
            flash(f'Add users  to view','info')    
    return render_template('manage_user.html', title = 'Manage User', details=details)

@bp.route("/location", methods = ['GET', 'POST'])
@login_required
def location():
    editform = EditLocationForm()
    addform = AddLocationForm()
    details = Location.query.all()
    exists = bool(Location.query.all())
    if exists== False and request.method == 'GET':
            flash(f'Add locations  to view','info')
    if editform.editsubmit.data and editform.validate() and request.method == 'POST':
        id = request.form.get("id","")
        name = request.form.get("name","")
        details = Location.query.all()
        loc = Location.query.filter_by(id = id).first()
        loc.name = editform.editname.data
        try:
            db.session.commit()
            flash(f'{editform.editname.data} has been updated!', 'success')
            return redirect(url_for('main.location'))
        except IntegrityError :
            db.session.rollback()
            flash(f'This location already exists','danger')
            return redirect(url_for('main.location'))
        
    elif addform.submit.data and addform.validate() :
        loc = Location(name=addform.name.data)
        db.session.add(loc)
        try:
            db.session.commit()
            flash(f'Your location {addform.name.data} has been added!', 'success')
            return redirect(url_for('main.location'))
        except IntegrityError :
            db.session.rollback()
            flash(f'This location already exists','danger')
            return redirect(url_for('main.location'))
    
    return render_template('location.html', title = 'Locations', editform=editform, addform=addform, details=details)

@bp.route("/category", methods = ['GET', 'POST'])
@login_required
def category():
    editform = EditCategoryForm()
    addform = AddCategoryForm()
    details = Category.query.all()
    exists = bool(Category.query.all())
    if exists== False and request.method == 'GET':
            flash(f'Add categories to view','info')
    if editform.editsubmit.data and editform.validate() and request.method == 'POST':
        id = request.form.get("id","")
        name = request.form.get("name","")
        details = Category.query.all()
        cat = Category.query.filter_by(id = id).first()
        cat.name = editform.editname.data
        try:
            db.session.commit()
            flash(f'{editform.editname.data} has been updated!', 'success')
            return redirect(url_for('main.category'))
        except IntegrityError :
            db.session.rollback()
            flash(f'This category already exists','danger')
            return redirect(url_for('main.category'))
        
    elif addform.submit.data and addform.validate() :
        cat = Category(name=addform.name.data)
        db.session.add(cat)
        try:
            db.session.commit()
            flash(f'Your location {addform.name.data} has been added!', 'success')
            return redirect(url_for('main.category'))
        except IntegrityError :
            db.session.rollback()
            flash(f'This category already exists','danger')
            return redirect(url_for('main.category'))
    
    return render_template('category.html', title = 'Category', editform=editform, addform=addform, details=details)


@bp.route("/product", methods = ['GET','POST'])
@login_required
def product():
    editform = EditProductForm()
    addform = AddProductForm()
    details = Product.query.all()
    exists = bool(Product.query.all())
    if exists== False and request.method == 'GET' :
            flash(f'Add products to view','info')
    
    cats = Category.query.with_entities(Category.name).order_by(Category.id).all()
    cats_list = []
    for cat in cats:
        cats_list.append(cat[-1])
    editform.editcategory.choices = cats_list
    addform.category.choices = cats_list
    
    if editform.editsubmit.data and editform.validate() and request.method == 'POST':
        id = request.form.get("id","")
        name = request.form.get("name","")
        category = request.form.get("category","")
        details = Product.query.all()
        prod = Product.query.filter_by(name = name).first()
        prod.name = editform.editname.data
        prod.qty= editform.editqty.data
        this_cat = Category.query.filter_by(name = editform.editcategory.data).first()
        prod.category_id = this_cat.id
        try:
            db.session.commit()
            flash(f'Your product [{name}] has been updated!', 'success')
            return redirect(url_for('main.product'))
        except IntegrityError :
            db.session.rollback()
            flash(f'This product already exists','danger')
            return redirect(url_for('main.product'))
    
    elif addform.submit.data and addform.validate():
        this_cat = Category.query.filter_by(name = addform.category.data).first()
        product = Product(name=addform.name.data,qty=addform.qty.data,
                          category_id=this_cat.id)
        db.session.add(product)
        try:
            db.session.commit()
            flash(f'Your product {addform.name.data} has been added!', 'success')
            return redirect(url_for('main.product'))
        except IntegrityError :
            db.session.rollback()
            flash(f'This product already exists','danger')
            return redirect(url_for('main.product'))
        
    return render_template('product.html',title = 'Products',editform=editform, \
                           addform = addform, details=details)


@bp.route("/delete")
@login_required
def delete():
    type = request.args.get('type')
    if type == 'product':
        id = request.args.get('id')
        product = Product.query.filter_by(id=id).delete()
        db.session.commit()
        flash(f'Your product has been deleted!', 'success')
        return redirect(url_for('main.product'))
        return render_template('product.html',title = 'Products')
    elif type == 'category':
        id = request.args.get('id')
        product = Category.query.filter_by(id=id).delete()
        db.session.commit()
        flash(f'Your category has been deleted!', 'success')
        return redirect(url_for('main.category'))
        return render_template('category.html',title = 'Categories')
    elif type == 'location':
        id = request.args.get('id')
        if int(id) == 1:
            flash(f'You can\'t delete Main Warehouse','danger')
            return redirect(url_for('main.location'))
        
        loc = Location.query.filter_by(id = id).delete()
        db.session.commit()
        flash(f'Your location has been deleted!', 'success')
        return redirect(url_for('main.location'))
        return render_template('location.html',title = 'Locations')
    elif type == 'user':
        if current_user.role_id != 1:
            flash(f'You don\'t have the permission','danger')
            return redirect(url_for('main.manage_user'))

        id = request.args.get('id')
        if int(id) == 1:
            flash(f'You can\'t delete this owner account','danger')
            return redirect(url_for('main.manage_user'))
        
        user = User.query.filter_by(id = id).delete()
        db.session.commit()
        flash(f'User {id} has been deleted!', 'success')
        return redirect(url_for('main.manage_user'))
        return render_template('manage_user.html',title = 'Manage User')
    
@bp.route("/transfer", methods = ['GET', 'POST'])
@login_required
def transfer():
    form = TransferProductForm()

    details = Transfer.query.all()
    exists = bool(Transfer.query.all())
    if exists== False and request.method == 'GET' :
            flash(f'Transfer products  to view','info')

    prods = Product.query.with_entities(Product.name).all()
    locs = Location.query.with_entities(Location.name).all()
    prods_list, locs_list = [], []
    
    for prod in prods:
        prods_list.append(prod[-1])
    form.product.choices = prods_list
    
    for loc in locs:
        locs_list.append(loc[-1])
    form.floc.choices = form.tloc.choices = locs_list
    
    if form.validate_on_submit() and request.method == 'POST' :
        timestamp = datetime.now()
        
        this_product = Product.query.filter_by(name = form.product.data).first()
        this_floc = Location.query.filter_by(name = form.floc.data).first()
        this_tloc = Location.query.filter_by(name = form.tloc.data).first()
        
        result = check(this_product, this_floc, this_tloc, form.qty.data)
        if result == 'insufficient_qty':
            flash(f'Insufficient amounts of [{this_product.name}]s in [{this_floc.name}], retry with lower amounts',
                  'danger')
        elif result == 'same_locs':
            flash(f'Both locations cannot be the same.', 'danger')
        elif result == 'no_product':
            flash(f'[{this_product.name}]s are not found in [{this_floc.name}]. Please add products', \
                  'danger')
        else:
            tf = Transfer(time=timestamp,floc_id=this_floc.id, tloc_id=this_tloc.id,
                           product_id=this_product.id, qty=form.qty.data)
            db.session.add(tf)
            db.session.commit()
            flash(f'Your transfer activity has been added!', 'success')
        return redirect(url_for('main.transfer'))
    return render_template('transfer.html',title = 'Transfers',form = form,details= details)

def check(product,floc,tloc,qty):
    if floc.name == tloc.name :
        return 'same_locs'
    
    elif floc.name == 'Main Warehouse' and tloc.name != 'Main Warehouse':
        prod_query = Product.query.filter_by(id=product.id).first()
        if prod_query.qty >= qty:
            prod_query.qty -= qty
            balance = Balance.query.filter_by(loc_id=tloc.id, product_id=product.id).first()
            if(str(balance) == 'None'):
                new_balance = Balance(product_id=product.id, loc_id=tloc.id, qty=qty)
                db.session.add(new_balance)
            else:
                balance.qty += qty
            db.session.commit()
        else :
            return 'insufficient_qty'
        
    elif floc.name != 'Main Warehouse' and tloc.name == 'Main Warehouse':
        balance = Balance.query.filter_by(loc_id=floc.id, product_id=product.id).first()
        if(str(balance)=='None'):
            return 'no_product'
        else:
            if balance.qty >= qty:
                prod_query = Product.query.filter_by(id=product.id).first()
                prod_query.qty += qty
                balance.qty -= qty
                db.session.commit()
            else :
                 return 'insufficient_qty'

    else:
        balance = Balance.query.filter_by(loc_id=floc.id, product_id=product.id).first()
        if(str(balance)=='None'):
            return 'no_product'

        elif balance.qty > qty:
            balance2 = Balance.query.filter_by(loc_id=tloc.id, product_id=product.id).first()
            if str(balance2) == 'None':
                new_balance2 = Balance(product_id=product.id, loc_id=tloc.id, qty=qty)
                db.session.add(new_balance2)
                balance.qty -= qty
                db.session.commit()
            else:
                balance2.qty += qty
                balance.qty -= qty
                db.session.commit()
        else:
                 return 'insufficient_qty'
                
@bp.route('/download')  
def download():
    if current_user.role_id not in (1,2):
        flash(f'You don\'t have the permission','danger')
        return redirect(url_for('main.index'))
    type = request.args.get('type')
    csv = ""
    t = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if type == 'product':
        title = 'product-'
        header = 'ID,Product Name,Category,Quantity\n'
        csv += header
        details = Product.query.all()
        for d in details:
            csv += str(d.id)
            csv += ','
            csv += d.name
            csv += ','
            csv += string(d.category)
            csv += ','
            csv += str(d.qty)
            csv += '\n'
    
    elif type == 'location':
        title = 'location-'
        header = 'ID,Location Name\n'
        csv += header
        details = Location.query.all()
        for d in details:
            csv += str(d.id)
            csv += ','
            csv += d.name
            csv += '\n'
            
    elif type == 'category':
        title = 'category-'
        header = 'ID,Category Name\n'
        csv += header
        details = Category.query.all()
        for d in details:
            csv += str(d.id)
            csv += ','
            csv += d.name
            csv += '\n'
            
    elif type == 'transfer':
        title = 'transfer-'
        header = 'ID,Time,From,To,Product Name,Quantity\n'
        csv += header
        details = Transfer.query.all()
        for d in details:
            csv += str(d.id)
            csv += ','
            csv += str(d.time)
            csv += ','
            csv += string(d.floc)
            csv += ','
            csv += string(d.tloc)
            csv += ','
            csv += string(d.product)
            csv += ','
            csv += str(d.qty)
            csv += '\n'
            
    elif type == 'balance':
        title = 'balance-'
        header = 'ID,Location,Product Name,Quantity\n'
        csv += header
        details = Balance.query.all()
        for d in details:
            csv += str(d.id)
            csv += ','
            csv += string(d.loc)
            csv += ','
            csv += string(d.product)
            csv += ','
            csv += str(d.qty)
            csv += '\n'
            
    elif type == 'user':
        title = 'user-'
        header = 'ID,Username,Email,Role\n'
        csv += header
        details = User.query.all()
        for d in details:
            csv += str(d.id)
            csv += ','
            csv += d.username
            csv += ','
            csv += d.email
            csv += ','
            csv += string(d.role)
            csv += '\n'
        
    response = make_response(csv)
    cd = 'attachment; filename=' + title + t +'-.csv'
    response.headers['Content-Disposition'] = cd 
    response.mimetype='text/csv'

    return response

def string(obj):
    try:
        return str(obj.name)
    except:
        return ''