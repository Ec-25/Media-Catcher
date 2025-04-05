from version import VER

translations = {
    "es": {
        "title": f"Media Catcher - Inicio - v{str(VER)}",
        "menu": {
            "file": "Archivo",
            "edit": "Editar",
            "language": "Idioma",
            "help": "Ayuda",
        },
        "menuActions": {
            "exit": "Salir",
            "saveHistory": "Guardar Historial",
            "configuration": "Configuración",
            "clearList": "Limpiar Lista",
            "about": "Acerca de"
        },
        "msg": {
            "savedHistory": "Historial guardado",
        },
        "about": {
            "title": "Acerca de",
            "text": f"Media Catcher v{str(VER)}\n\nDesarrollado por ec25\n\nEsta aplicación te permite administrar y descargar contenido multimedia.\n\nRepositorio: https://github.com/Ec-25/media-catcher"
        },
        "configuration": {
            "title": "Configuración de Media Catcher",
            "save": "Guardar",
            "cancel": "Cancelar",
            "saved": "Configuración guardada"
        },
        "errors": {
            "not_found": "No se encontró el archivo de configuración.",
            "dependencies_not_found": "No se encontraron las dependencias necesarias. Por favor, instálalo manualmente.\nPara instalar las dependencias faltantes, ejecuta el siguiente comando:\n",
            "download_dep":  "Error al descargar las dependencias. Por favor, verifica tu conexión a internet e inténtalo de nuevo.",
            "invalid_url": "La URL ingresada no es válida.",
            "extract_info": "Error al extraer información del contenido multimedia."
        },
        "elements": {
            "placeHolders": {
                "inputUrl": "URL del contenido multimedia"
            },
            "buttons": {
                "add": "Agregar"
            },
            "table_model": {
                "title": "Título o URL",
                "duration": "Duración",
                "size": "Tamaño",
                "downloaded": "Descargado",
                "time_remaining": "Tiempo Restante"
            },
            "item_table": {
                "delete_question": {
                    "title": "Eliminar elemento",
                    "text": "¿Estás seguro de que quieres eliminar este elemento?"
                }
            }
        }
    },
    "en": {
        "title": f"Media Catcher - Home - v{str(VER)}",
        "menu": {
            "file": "File",
            "edit": "Edit",
            "language": "Language",
            "help": "Help",
        },
        "menuActions": {
            "exit": "Exit",
            "saveHistory": "Save History",
            "configuration": "Configuration",
            "clearList": "Clear List",
            "about": "About"
        },
        "msg": {
            "savedHistory": "History saved",
        },
        "about": {
            "title": "About",
            "text": f"Media Catcher v{str(VER)}\n\nDeveloped by ec25\n\nThis application allows you to manage and download multimedia content.\n\nRepository: https://github.com/Ec-25/media-catcher"
        },
        "configuration": {
            "title": "Media Catcher Configuration",
            "save": "Save",
            "cancel": "Cancel",
            "saved": "Configuration saved"
        },
        "errors": {
            "not_found": "Configuration file not found.",
            "dependencies_not_found": "The required dependencies were not found. Please install it manually.\nTo install the missing dependencies, run the following command:\n",
            "download_dep":  "Error downloading dependencies. Please check your internet connection and try again.",
            "invalid_url": "The entered URL is not valid.",
            "extract_info": "Error extracting multimedia content information."
        },
        "elements": {
            "placeHolders": {
                "inputUrl": "URL of the multimedia content"
            },
            "buttons": {
                "add": "Add"
            },
            "table_model": {
                "title": "Title or URL",
                "duration": "Duration",
                "size": "Size",
                "downloaded": "Downloaded",
                "time_remaining": "Time Remaining"
            },
            "item_table": {
                "delete_question": {
                    "title": "Delete item",
                    "text": "Are you sure you want to delete this item?"
                }
            }
        }
    }
}
