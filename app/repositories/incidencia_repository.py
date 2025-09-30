from app.core.supabase_client import supabase

class IncidenciaRepository:
    def __init__(self):
        self.nombre_tabla = "incidencias"

    async def crear_incidencia(self, datos_incidencia: dict):
        response = supabase.table(self.nombre_tabla).insert(datos_incidencia).execute()
        return response.data

    async def obtener_incidencias(self): #fixear para que solo agarre las cosas importantes
        response = supabase.table(self.nombre_tabla).select("*").execute()
        return response.data
    
    async def obtener_incidencia_por_id(self, id_incidencia: int):
        response = supabase.table(self.nombre_tabla).select("*").eq("id", id_incidencia).execute()
        return response.data
    
    async def actualizar_incidencia(self, id_incidencia: int, datos_actualizados: dict):
        response = supabase.table(self.nombre_tabla).update(datos_actualizados).eq("id", id_incidencia).execute()
        return response.data
    
    async def eliminar_incidencia(self, id_incidencia: int):
        response = supabase.table(self.nombre_tabla).delete().eq("id", id_incidencia).execute()
        return response.data
    