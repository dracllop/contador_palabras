"""
Pruebas unitarias para la clase ValidadorArchivo
"""
import os
import tempfile
import pytest
from contador import ValidadorArchivo


class TestValidadorArchivo:
    """Clase de pruebas para ValidadorArchivo"""
    
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.temp_dir = tempfile.mkdtemp()
        self.archivo_prueba = os.path.join(self.temp_dir, "test.txt")
        
        # Crear archivo de prueba
        with open(self.archivo_prueba, 'w', encoding='utf-8') as f:
            f.write("Este es un archivo de prueba")
    
    def teardown_method(self):
        """Limpieza después de cada prueba"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    @pytest.mark.unit
    def test_validar_ruta_archivo_exitoso(self):
        """Prueba validación exitosa de archivo existente"""
        es_valida, mensaje = ValidadorArchivo.validar_ruta_archivo(self.archivo_prueba)
        
        assert es_valida is True
        assert mensaje == ""
    
    @pytest.mark.unit
    def test_validar_ruta_archivo_vacio(self):
        """Prueba validación con ruta vacía"""
        es_valida, mensaje = ValidadorArchivo.validar_ruta_archivo("")
        
        assert es_valida is False
        assert "Debe ingresar una ruta de archivo" in mensaje
    
    @pytest.mark.unit
    def test_validar_ruta_archivo_inexistente(self):
        """Prueba validación con archivo que no existe"""
        ruta_inexistente = os.path.join(self.temp_dir, "no_existe.txt")
        es_valida, mensaje = ValidadorArchivo.validar_ruta_archivo(ruta_inexistente)
        
        assert es_valida is False
        assert "No se encontró" in mensaje
        assert "no_existe.txt" in mensaje
    
    @pytest.mark.unit
    def test_validar_ruta_carpeta(self):
        """Prueba validación con ruta que es una carpeta"""
        es_valida, mensaje = ValidadorArchivo.validar_ruta_archivo(self.temp_dir)
        
        assert es_valida is False
        assert "es una carpeta, no un archivo" in mensaje
    
    @pytest.mark.unit
    def test_buscar_archivos_similares_exitoso(self):
        """Prueba búsqueda de archivos similares"""
        # Crear archivos con nombres similares
        archivo1 = os.path.join(self.temp_dir, "test_similar.txt")
        archivo2 = os.path.join(self.temp_dir, "test_diferente.txt")
        archivo3 = os.path.join(self.temp_dir, "otro_archivo.txt")
        
        for archivo in [archivo1, archivo2, archivo3]:
            with open(archivo, 'w') as f:
                f.write("contenido")
        
        similares = ValidadorArchivo.buscar_archivos_similares("test", self.temp_dir)
        
        assert "test_similar.txt" in similares
        assert "test_diferente.txt" in similares
        assert "otro_archivo.txt" not in similares
    
    @pytest.mark.unit
    def test_buscar_archivos_similares_vacio(self):
        """Prueba búsqueda de archivos similares sin resultados"""
        similares = ValidadorArchivo.buscar_archivos_similares("inexistente", self.temp_dir)
        
        assert similares == []
    
    @pytest.mark.unit
    def test_buscar_archivos_similares_carpeta_inexistente(self):
        """Prueba búsqueda en carpeta que no existe"""
        similares = ValidadorArchivo.buscar_archivos_similares("test", "/carpeta/inexistente")
        
        assert similares == []
    
    @pytest.mark.unit
    def test_generar_mensaje_archivo_no_encontrado_carpeta_existe(self):
        """Prueba generación de mensaje cuando la carpeta existe pero no el archivo"""
        ruta_inexistente = os.path.join(self.temp_dir, "no_existe.txt")
        mensaje = ValidadorArchivo._generar_mensaje_archivo_no_encontrado(ruta_inexistente)
        
        assert "No se encontró" in mensaje
        assert "SÍ existe" in mensaje
        assert "no_existe.txt" in mensaje
        assert "test.txt" in mensaje  # Debe mostrar el archivo que sí existe
    
    @pytest.mark.unit
    def test_generar_mensaje_archivo_no_encontrado_carpeta_inexistente(self):
        """Prueba generación de mensaje cuando la carpeta no existe"""
        ruta_inexistente = "/carpeta/inexistente/archivo.txt"
        mensaje = ValidadorArchivo._generar_mensaje_archivo_no_encontrado(ruta_inexistente)
        
        assert "No se encontró" in mensaje
        assert "NO existe" in mensaje
        assert "Sugerencias:" in mensaje
