"""
Pruebas unitarias para la clase ContadorPalabras
"""
import os
import tempfile
import pytest
from contador import ContadorPalabras


class TestContadorPalabras:
    """Clase de pruebas para ContadorPalabras"""
    
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.contador = ContadorPalabras()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Limpieza después de cada prueba"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _crear_archivo_prueba(self, nombre, contenido):
        """Método auxiliar para crear archivos de prueba"""
        ruta = os.path.join(self.temp_dir, nombre)
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        return ruta
    
    @pytest.mark.unit
    def test_procesar_archivo_exitoso(self):
        """Prueba procesamiento exitoso de archivo"""
        contenido = "Hola mundo esta es una prueba"
        archivo = self._crear_archivo_prueba("test.txt", contenido)
        
        exito, mensaje = self.contador.procesar_archivo(archivo)
        
        assert exito is True
        assert mensaje == ""
        assert self.contador.numero_total_palabras == 6
        assert len(self.contador.palabras) == 6
        assert "Hola" in self.contador.palabras
        assert "mundo" in self.contador.palabras
    
    @pytest.mark.unit
    def test_procesar_archivo_vacio(self):
        """Prueba procesamiento de archivo vacío"""
        archivo = self._crear_archivo_prueba("vacio.txt", "")
        
        exito, mensaje = self.contador.procesar_archivo(archivo)
        
        assert exito is True
        assert mensaje == ""
        assert self.contador.numero_total_palabras == 0
        assert len(self.contador.palabras) == 0
    
    @pytest.mark.unit
    def test_procesar_archivo_inexistente(self):
        """Prueba procesamiento de archivo que no existe"""
        archivo_inexistente = os.path.join(self.temp_dir, "no_existe.txt")
        
        exito, mensaje = self.contador.procesar_archivo(archivo_inexistente)
        
        assert exito is False
        assert "Error al procesar el archivo" in mensaje
    
    @pytest.mark.unit
    def test_procesar_archivo_con_acentos(self):
        """Prueba procesamiento de archivo con caracteres especiales"""
        contenido = "café corazón acción"
        archivo = self._crear_archivo_prueba("acentos.txt", contenido)
        
        exito, mensaje = self.contador.procesar_archivo(archivo)
        
        assert exito is True
        assert mensaje == ""
        assert self.contador.numero_total_palabras == 3
        assert "café" in self.contador.palabras
        assert "corazón" in self.contador.palabras
        assert "acción" in self.contador.palabras
    
    @pytest.mark.unit
    def test_procesar_archivo_con_numeros(self):
        """Prueba procesamiento de archivo con números"""
        contenido = "123 456 789 palabra"
        archivo = self._crear_archivo_prueba("numeros.txt", contenido)
        
        exito, mensaje = self.contador.procesar_archivo(archivo)
        
        assert exito is True
        assert mensaje == ""
        assert self.contador.numero_total_palabras == 4
        assert "123" in self.contador.palabras
        assert "456" in self.contador.palabras
        assert "789" in self.contador.palabras
        assert "palabra" in self.contador.palabras
    
    @pytest.mark.unit
    def test_procesar_archivo_con_simbolos(self):
        """Prueba procesamiento de archivo con símbolos"""
        contenido = "¡Hola! ¿Cómo estás? @#$%"
        archivo = self._crear_archivo_prueba("simbolos.txt", contenido)
        
        exito, mensaje = self.contador.procesar_archivo(archivo)
        
        assert exito is True
        assert mensaje == ""
        assert self.contador.numero_total_palabras == 4
        assert "¡Hola!" in self.contador.palabras
        assert "¿Cómo" in self.contador.palabras
        assert "estás?" in self.contador.palabras
        assert "@#$%" in self.contador.palabras
    
    @pytest.mark.unit
    def test_obtener_estadisticas_archivo_normal(self):
        """Prueba obtención de estadísticas de archivo normal"""
        contenido = "palabra palabra otra"
        archivo = self._crear_archivo_prueba("estadisticas.txt", contenido)
        
        self.contador.procesar_archivo(archivo)
        estadisticas = self.contador.obtener_estadisticas()
        
        assert estadisticas['numero_total_palabras'] == 3
        assert estadisticas['archivo_vacio'] is False
        assert len(estadisticas['palabras_mas_frecuentes']) == 2
        assert estadisticas['palabras_mas_frecuentes'][0] == ('palabra', 2)
        assert estadisticas['palabras_mas_frecuentes'][1] == ('otra', 1)
    
    @pytest.mark.unit
    def test_obtener_estadisticas_archivo_vacio(self):
        """Prueba obtención de estadísticas de archivo vacío"""
        archivo = self._crear_archivo_prueba("vacio.txt", "")
        
        self.contador.procesar_archivo(archivo)
        estadisticas = self.contador.obtener_estadisticas()
        
        assert estadisticas['numero_total_palabras'] == 0
        assert estadisticas['archivo_vacio'] is True
        assert len(estadisticas['palabras_mas_frecuentes']) == 0
    
    @pytest.mark.unit
    def test_obtener_estadisticas_mas_de_10_palabras(self):
        """Prueba obtención de estadísticas con más de 10 palabras únicas"""
        contenido = " ".join([f"palabra{i}" for i in range(15)])
        archivo = self._crear_archivo_prueba("muchas_palabras.txt", contenido)
        
        self.contador.procesar_archivo(archivo)
        estadisticas = self.contador.obtener_estadisticas()
        
        assert estadisticas['numero_total_palabras'] == 15
        assert estadisticas['archivo_vacio'] is False
        assert len(estadisticas['palabras_mas_frecuentes']) == 10  # Solo las 10 más frecuentes
    
    @pytest.mark.unit
    def test_mostrar_resultados_archivo_normal(self, capsys):
        """Prueba mostrar resultados de archivo normal"""
        contenido = "palabra palabra otra"
        archivo = self._crear_archivo_prueba("mostrar.txt", contenido)
        
        self.contador.procesar_archivo(archivo)
        self.contador.mostrar_resultados(archivo)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Archivo procesado exitosamente" in output
        assert "El número total de palabras es: 3" in output
        assert "Las 10 palabras más frecuentes son:" in output
        assert "palabra" in output
        assert "otra" in output
    
    @pytest.mark.unit
    def test_mostrar_resultados_archivo_vacio(self, capsys):
        """Prueba mostrar resultados de archivo vacío"""
        archivo = self._crear_archivo_prueba("vacio.txt", "")
        
        self.contador.procesar_archivo(archivo)
        self.contador.mostrar_resultados(archivo)
        
        captured = capsys.readouterr()
        output = captured.out
        
        assert "Archivo procesado exitosamente" in output
        assert "El número total de palabras es: 0" in output
        assert "El archivo está vacío o no contiene palabras" in output
    
    @pytest.mark.unit
    def test_procesar_archivo_binario(self):
        """Prueba procesamiento de archivo binario (debe fallar)"""
        archivo_binario = os.path.join(self.temp_dir, "binario.bin")
        with open(archivo_binario, 'wb') as f:
            f.write(b'\x00\x01\x02\x03')
        
        exito, mensaje = self.contador.procesar_archivo(archivo_binario)
        
        assert exito is False
        assert "Error al procesar el archivo" in mensaje
    
    @pytest.mark.unit
    def test_procesar_archivo_con_saltos_linea(self):
        """Prueba procesamiento de archivo con saltos de línea"""
        contenido = "primera línea\nsegunda línea\ntercera línea"
        archivo = self._crear_archivo_prueba("saltos.txt", contenido)
        
        exito, mensaje = self.contador.procesar_archivo(archivo)
        
        assert exito is True
        assert mensaje == ""
        assert self.contador.numero_total_palabras == 6
        assert "primera" in self.contador.palabras
        assert "línea" in self.contador.palabras
        assert self.contador.palabras.count("línea") == 3
