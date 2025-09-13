# Programa para contar palabras en un archivo de texto
# Refactorizado con programación orientada a objetos

import os
import glob
from collections import Counter
from typing import List, Tuple, Optional


class ValidadorArchivo:
    """Clase responsable de validar archivos y rutas"""
    
    @staticmethod
    def buscar_archivos_similares(nombre_buscado: str, ruta_padre: str) -> List[str]:
        """Busca archivos con nombres similares al buscado"""
        archivos_similares = []
        try:
            archivos_en_carpeta = os.listdir(ruta_padre)
            nombre_buscado_lower = nombre_buscado.lower()
            
            for archivo in archivos_en_carpeta:
                archivo_lower = archivo.lower()
                # Buscar archivos que contengan parte del nombre buscado
                if (nombre_buscado_lower in archivo_lower or 
                    archivo_lower in nombre_buscado_lower or
                    archivo_lower.startswith(nombre_buscado_lower.split('.')[0])):
                    archivos_similares.append(archivo)
        except:
            pass
        
        return archivos_similares
    
    @staticmethod
    def validar_ruta_archivo(ruta_archivo: str) -> Tuple[bool, str]:
        """
        Valida si la ruta del archivo es válida
        Retorna: (es_valida, mensaje_error)
        """
        if not ruta_archivo.strip():
            return False, "❌ Error: Debe ingresar una ruta de archivo."
        
        if not os.path.exists(ruta_archivo):
            return False, ValidadorArchivo._generar_mensaje_archivo_no_encontrado(ruta_archivo)
        
        if not os.path.isfile(ruta_archivo):
            return False, f"❌ Error: '{ruta_archivo}' es una carpeta, no un archivo."
        
        return True, ""
    
    @staticmethod
    def _generar_mensaje_archivo_no_encontrado(ruta_archivo: str) -> str:
        """Genera un mensaje detallado cuando no se encuentra un archivo"""
        mensaje = f"❌ Error: No se encontró '{ruta_archivo}'\n"
        
        ruta_padre = os.path.dirname(ruta_archivo)
        nombre_archivo = os.path.basename(ruta_archivo)
        
        if ruta_padre and os.path.exists(ruta_padre):
            mensaje += f"   📁 La carpeta '{ruta_padre}' SÍ existe\n"
            mensaje += f"   📄 Pero el archivo '{nombre_archivo}' NO se encuentra en esa carpeta\n"
            
            try:
                archivos_en_carpeta = os.listdir(ruta_padre)
                archivos_txt = [f for f in archivos_en_carpeta if f.lower().endswith('.txt')]
                
                # Buscar archivos con nombres similares
                archivos_similares = ValidadorArchivo.buscar_archivos_similares(nombre_archivo, ruta_padre)
                
                if archivos_similares:
                    mensaje += f"   🔍 Archivos con nombres similares a '{nombre_archivo}':\n"
                    for archivo in archivos_similares:
                        mensaje += f"      - {archivo}\n"
                
                if archivos_txt:
                    mensaje += f"   📋 Archivos .txt disponibles en '{ruta_padre}':\n"
                    for archivo in archivos_txt:
                        mensaje += f"      - {archivo}\n"
                else:
                    mensaje += f"   📋 No hay archivos .txt en '{ruta_padre}'\n"
                    mensaje += f"   📋 Archivos disponibles: {', '.join(archivos_en_carpeta[:5])}\n"
                    if len(archivos_en_carpeta) > 5:
                        mensaje += f"      ... y {len(archivos_en_carpeta) - 5} archivos más\n"
            except PermissionError:
                mensaje += f"   ⚠️  No se puede acceder al contenido de '{ruta_padre}'\n"
        else:
            mensaje += f"   📁 La carpeta '{ruta_padre}' NO existe\n"
            mensaje += "   💡 Sugerencias:\n"
            mensaje += "      - Verifique que escribió la ruta correctamente\n"
            mensaje += "      - Use rutas absolutas como: /ruta/completa/al/archivo.txt\n"
            mensaje += "      - O rutas relativas como: ./archivo.txt\n"
        
        return mensaje


class ContadorPalabras:
    """Clase responsable de contar palabras en archivos"""
    
    def __init__(self):
        self.contenido = ""
        self.palabras = []
        self.numero_total_palabras = 0
        self.contador_palabras = Counter()
    
    def procesar_archivo(self, ruta_archivo: str) -> Tuple[bool, str]:
        """
        Procesa un archivo y cuenta las palabras
        Retorna: (exito, mensaje_error)
        """
        try:
            # Leer el contenido del archivo
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                self.contenido = archivo.read()
            
            # Separar en palabras
            self.palabras = self.contenido.split()
            
            # Contar número total de palabras
            self.numero_total_palabras = len(self.palabras)
            
            # Contar frecuencia de palabras
            self.contador_palabras = Counter(self.palabras)
            
            return True, ""
            
        except UnicodeDecodeError:
            return False, "❌ Error: No se puede leer el archivo. Puede que no sea un archivo de texto válido."
        except Exception as e:
            return False, f"❌ Error al procesar el archivo: {e}"
    
    def obtener_estadisticas(self) -> dict:
        """Retorna un diccionario con las estadísticas del archivo"""
        palabras_mas_frecuentes = self.contador_palabras.most_common(10)
        
        return {
            'numero_total_palabras': self.numero_total_palabras,
            'palabras_mas_frecuentes': palabras_mas_frecuentes,
            'archivo_vacio': self.numero_total_palabras == 0
        }
    
    def mostrar_resultados(self, ruta_archivo: str) -> None:
        """Muestra los resultados del conteo de palabras"""
        estadisticas = self.obtener_estadisticas()
        
        print(f"\n✅ Archivo procesado exitosamente: {ruta_archivo}")
        print(f"📊 El número total de palabras es: {estadisticas['numero_total_palabras']}")
        
        if not estadisticas['archivo_vacio']:
            print(f"\n🔝 Las 10 palabras más frecuentes son:")
            for i, (palabra, frecuencia) in enumerate(estadisticas['palabras_mas_frecuentes'], 1):
                print(f"  {i:2d}. '{palabra}' - {frecuencia} veces")
        else:
            print("⚠️  El archivo está vacío o no contiene palabras.")


class InterfazUsuario:
    """Clase responsable de la interacción con el usuario"""
    
    def __init__(self):
        self.validador = ValidadorArchivo()
        self.contador = ContadorPalabras()
    
    def mostrar_bienvenida(self) -> None:
        """Muestra el mensaje de bienvenida y ejemplos"""
        print("\n=== CONTADOR DE PALABRAS ===")
        print("El programa acepta archivos de texto (.txt)")
        print("Ejemplos de rutas válidas:")
        print("- /home/usuario/Documentos/mi_archivo.txt")
        print("- ./archivo.txt")
        print("- archivo.txt (si está en la misma carpeta)")
        print("\n💡 Escriba 'salir' o 'quit' para terminar el programa")
    
    def solicitar_ruta_archivo(self) -> str:
        """Solicita al usuario la ruta del archivo"""
        return input("\nIngrese la ruta del archivo de texto: ").strip()
    
    def validar_extension_archivo(self, ruta_archivo: str) -> bool:
        """Valida la extensión del archivo y pregunta al usuario si continuar"""
        if not ruta_archivo.lower().endswith('.txt'):
            respuesta = input(f"⚠️  El archivo '{ruta_archivo}' no tiene extensión .txt. ¿Continuar? (s/n): ").lower()
            return respuesta in ['s', 'si', 'sí', 'y', 'yes']
        return True
    
    def procesar_archivo(self, ruta_archivo: str) -> bool:
        """
        Procesa un archivo completo
        Retorna: True si se procesó exitosamente, False si hubo error
        """
        # Validar ruta
        es_valida, mensaje_error = self.validador.validar_ruta_archivo(ruta_archivo)
        if not es_valida:
            print(mensaje_error)
            return False
        
        # Validar extensión
        if not self.validar_extension_archivo(ruta_archivo):
            return False
        
        # Procesar archivo
        exito, mensaje_error = self.contador.procesar_archivo(ruta_archivo)
        if not exito:
            print(mensaje_error)
            return False
        
        # Mostrar resultados
        self.contador.mostrar_resultados(ruta_archivo)
        return True
    
    def preguntar_continuar(self) -> bool:
        """Pregunta al usuario si desea procesar otro archivo"""
        continuar = input("\n¿Desea procesar otro archivo? (s/n): ").lower()
        return continuar in ['s', 'si', 'sí', 'y', 'yes']
    
    def mostrar_despedida(self) -> None:
        """Muestra mensaje de despedida"""
        print("\n👋 ¡Gracias por usar el contador de palabras!")


class Aplicacion:
    """Clase principal que coordina toda la aplicación"""
    
    def __init__(self):
        self.interfaz = InterfazUsuario()
    
    def ejecutar(self) -> None:
        """Método principal que ejecuta la aplicación"""
        self.interfaz.mostrar_bienvenida()
        
        while True:
            ruta_archivo = self.interfaz.solicitar_ruta_archivo()
            
            # Verificar si el usuario quiere salir
            if ruta_archivo.lower() in ['salir', 'quit', 'exit', 'q']:
                break
            
            # Procesar archivo
            self.interfaz.procesar_archivo(ruta_archivo)
            
            # Preguntar si continuar
            if not self.interfaz.preguntar_continuar():
                break
        
        self.interfaz.mostrar_despedida()


# Punto de entrada principal
if __name__ == "__main__":
    app = Aplicacion()
    app.ejecutar()