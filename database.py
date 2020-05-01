import datetime
import mysql.connector
from flask import session
from datetime import date
from datetime import timedelta
from datetime import datetime
def db_connect():
    _conn = mysql.connector.connect(host="localhost", user='root',
                            password='', db='srija')
    c = _conn.cursor()

    return c, _conn
def storedata(name, fname, dob, hno, colony, location, mandal, dist, pin, rta, photo, usersign, authoritysign, ref, vtype, badge, bloodgroup):
    try:
        c, conn = db_connect()
        today = date.today()
        issue = today.strftime("%d/%m/%Y")
        year = datetime.now()+timedelta(days=7300+5)  # Added 20Years In Current Date
        val = year.strftime("%d/%m/%Y")
        c.execute("insert into userdata (name,fname,dob,hno,colony,location,mandal,dist,pin,issue,validity,rta,photo,usersign,authoritysign,ref,vtype,badge,bloodgroup) values ('"+name+"','"+fname+"','"+dob +
                      "','"+hno+"','"+colony+"','"+location+"','"+mandal+"','"+dist+"','"+pin+"','"+issue+"','"+val+"','"+rta+"','"+photo+"','"+usersign+"','"+authoritysign+"','"+ref+"','"+vtype+"','"+badge+"','"+bloodgroup+"')")
        j= c.rowcount
        conn.commit()
        c.close()
        conn.close()
        return j
    except mysql.connector.Error as e:
        return(str(e))
def eloginact(username, password):
    try:
        c, conn = db_connect()
        c.execute("select * from employee where username='" +
                      username + "' and pass='" + password + "'")
        result =c.fetchone()
        c.close()
        conn.close()
        return result
    except mysql.connector.Error as e:
        return (str(e))
def vlicences():
    c, conn = db_connect()
    c.execute("select * from userdata")
    result = c.fetchall()
    xyz=len(result)
    c.close()
    conn.close()
    return result,xyz
def vlicence(id):
    c, conn = db_connect()
    id1=str(id)
    c.execute("select * from userdata where id='"+id1+"'")
    result = c.fetchone()
    c.close()
    conn.close()
    return result
def returnid(name):
    c, conn = db_connect()
    c.execute("select id from userdata where name='"+name+"'")
    id1=c.fetchone()
    id=id1[0]
    c.close()
    conn.close()
    return id


if __name__ == "__main__":
    print(db_connect())


