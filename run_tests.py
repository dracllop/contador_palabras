#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas del contador de palabras
"""
import subprocess
import sys
import os


def run_tests():
    """Ejecuta todas las pruebas"""
    print("🧪 Ejecutando batería de pruebas del contador de palabras...")
    print("=" * 60)
    
    # Verificar que pytest esté instalado
    try:
        import pytest
    except ImportError:
        print("❌ Error: pytest no está instalado.")
        print("Instale las dependencias con: pip install -r requirements.txt")
        return False
    
    # Ejecutar pruebas unitarias
    print("\n📋 Ejecutando pruebas unitarias...")
    result_unit = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-m", "unit",
        "-v",
        "--tb=short"
    ], capture_output=True, text=True)
    
    if result_unit.returncode == 0:
        print("✅ Pruebas unitarias: PASARON")
    else:
        print("❌ Pruebas unitarias: FALLARON")
        print(result_unit.stdout)
        print(result_unit.stderr)
    
    # Ejecutar pruebas de integración
    print("\n🔗 Ejecutando pruebas de integración...")
    result_integration = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-m", "integration",
        "-v",
        "--tb=short"
    ], capture_output=True, text=True)
    
    if result_integration.returncode == 0:
        print("✅ Pruebas de integración: PASARON")
    else:
        print("❌ Pruebas de integración: FALLARON")
        print(result_integration.stdout)
        print(result_integration.stderr)
    
    # Ejecutar todas las pruebas con cobertura
    print("\n📊 Ejecutando todas las pruebas con cobertura...")
    result_coverage = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "--cov=contador",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v"
    ], capture_output=True, text=True)
    
    if result_coverage.returncode == 0:
        print("✅ Todas las pruebas: PASARON")
        print("\n📈 Reporte de cobertura generado en htmlcov/index.html")
    else:
        print("❌ Algunas pruebas: FALLARON")
        print(result_coverage.stdout)
        print(result_coverage.stderr)
    
    # Resumen final
    print("\n" + "=" * 60)
    if result_unit.returncode == 0 and result_integration.returncode == 0:
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
