from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# 1 สร้าง server ง่ายๆ
app = Flask(__name__) 

# 7. เพิ่ม code ด้านล่าง
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystatement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 8. สร้าง model เพื่อจัดการข้อมูลเป็นตาราง
class Statement(db.Model):
    id  = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(50),nullable=False)
    name = db.Column(db.String(100),nullable=False)
    prices = db.Column(db.Integer,nullable=False)
    amount = db.Column(db.Integer,nullable=False)
    category = db.Column(db.String(50),nullable=False)

# 9. สร้าง database ขึ้นเเละสร้างตาราง
with app.app_context():
    db.create_all()

# 12.สร้างฟังก์ชันจัดการเรื่องของสกุลเงิน
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "{:,.2f}".format(value)

# 3 สร้าง route
@app.route("/addForm")
def addForm():
    return render_template("addForm.html")

# 4 สร้าง route เพิ่มรับข้อมูลในหน้้า add statement เข้ามาใน server
@app.route("/addStatement", methods=['POST'])
def addStatement():
    # 5. รับค่ากี่ค่าก็สร้างตัวเเปรมารับ date ด้านหลังมาจาก ชื่อ name="date" ในหน้า addForm
    date = request.form["date"]
    name = request.form["name"]
    prices = request.form["prices"]
    amount = request.form["amount"]
    category = request.form["category"]

    # 10. เพิ่มข้อมูลเมื่อกด summit
    statement = Statement(date=date, name=name, prices=prices, amount=amount, category=category)
    db.session.add(statement)
    db.session.commit()
    return redirect("/")

# 11 .เเสดงผล เพื่อที่จะโยนไปที่หน้า statement.html
@app.route("/")
def showData():
    statements = Statement.query.all()
    return render_template("statements.html", statements=statements)

# 13. สร้างฟังก์ชันเมื่อกดปุ่มลบ
@app.route("/delete/<int:id>")
def deleteStatemant(id):
    statement = Statement.query.filter_by(id=id).first()
    db.session.delete(statement)
    db.session.commit()
    return redirect("/")

# 14. สร้างฟังก์ชันเพื่อเเก้ไขข้อมูล
@app.route("/edit/<int:id>")
def editStatement(id):
    statement = Statement.query.filter_by(id=id).first()
    return render_template("editForm.html", statement=statement)

# 15. การสร้างฟังก์ชันเพิ่มอัพเดทข้อมูล
@app.route("/updateStatement", methods=['POST'])
def updateStatement():
    id = request.form["id"]
    date = request.form["date"]
    name = request.form["name"]
    prices = request.form["prices"]
    amount = request.form["amount"]
    category = request.form["category"]
    statement = Statement.query.filter_by(id=id).first()
    statement.date=date
    statement.name=name
    statement.prices=prices
    statement.amount=amount
    statement.category=category
    db.session.commit()
    return redirect("/")


# 2 รัน server
if __name__  == "__main__":
    app.run(debug=True)