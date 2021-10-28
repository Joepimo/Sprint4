import db 
from werkzeug.security import generate_password_hash, check_password_hash

class usuario():
    nombre =''
    usuario=''
    correo=''
    password=''

    def __init__(self, p_nombre, p_usuario, p_correo, p_password):
        self.nombre = p_nombre
        self.usuario = p_usuario
        self.correo = p_correo
        self.password = p_password
    
    #Utilizamos un metodo de clase para crear una sobrecarga
    #del constructor de usuario, donde enviando el username 
    #buscamos en la base de datos y obtenemos su información.
    @classmethod
    def cargar(cls, p_usuario):
        sql = "SELECT * FROM usuarios WHERE usuario = ?;"
        obj = db.ejecutar_select(sql, [ p_usuario ])
        if obj:
            if len(obj)>0:
                #Llamamos al constructor de la clase para 
                #devolver una instancia de usuario
                #(p_nombre, p_usuario, p_correo, p_password)
                return cls(obj[0]["nombre"], obj[0]["usuario"], obj[0]["correo"], obj[0]["password"])

        return None

    #Metodo para insertar el usuario en la base de datos
    def insertar(self):
        #Preparamos el comando INSERT para guardar el usuario en la base de datos.
        sql = "INSERT INTO usuarios (usuario,nombre,correo,password) VALUES (?, ?, ?, ?);"
        #Invocamos a la función generate_password_hash para generar el hash seguro del password 
        #del usuario y poder almacenarlo en nuestra bd.
        hashed_pwd = generate_password_hash(self.password, method="pbkdf2:sha256", salt_length=32)
        afectadas = db.ejecutar_insert(sql, [ self.usuario, self.nombre, self.correo, hashed_pwd ])
        return (afectadas > 0)


    def verificar(self):
        
        sql = "SELECT * FROM usuarios WHERE usuario = ?; "
        
        obj_usuario = db.ejecutar_select(sql, [ self.usuario ])

        if obj_usuario:
            if len(obj_usuario) >0:
                
                if check_password_hash(obj_usuario[0]["password"], self.password):
                    return True
        
        return False

class mensaje():
    id=0
    nombre=''
    correo=''
    mensaje=''
    respuesta=''
    estado=''

    
    def __init__(self, p_id, p_nombre, p_correo, p_mensaje, p_respuesta='', p_estado ='S'):
        self.id = p_id
        self.nombre = p_nombre
        self.correo = p_correo
        self.mensaje = p_mensaje
        self.respuesta = p_respuesta
        self.estado = p_estado
    
    
    @classmethod
    def cargar(cls, p_id):
        sql = "SELECT * FROM mensajes WHERE id = ?;"
        obj = db.ejecutar_select(sql, [ p_id ])
        if obj:
            if len(obj)>0:
                
                return cls(obj[0]["id"], obj[0]["nombre"], obj[0]["correo"], obj[0]["mensaje"], obj[0]["respuesta"], obj[0]["estado"])

        return None

    
    def insertar(self):
        sql = "INSERT INTO mensajes (nombre, correo, mensaje, estado) VALUES (?,?,?,?);"
        afectadas = db.ejecutar_insert(sql, [ self.nombre, self.correo, self.mensaje, 'S' ])
        return (afectadas >0)

    
    def eliminar(self):
        sql = "DELETE mensajes WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.id ])
        return (afectadas >0)

    def responder(self):
        sql = "UPDATE mensajes SET respuesta = ?, estado='R' WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.respuesta, self.id ])
        return (afectadas >0)


    @staticmethod
    def listado():
        sql = "SELECT * FROM mensajes ORDER BY id;"
        return db.ejecutar_select(sql, None)