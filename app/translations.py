from version import __version__

translations = {
    "es": {
        "title": f"Media Catcher - v{__version__}",
        "menu": {
            "file": "Archivo",
            "edit": "Editar",
            "language": "Idioma",
            "downloads": "Descargas",
            "help": "Ayuda",
        },
        "menuActions": {
            "exit": "Salir",
            "switch": "Mostrar/Ocultar",
            "history": "Historial",
            "configuration": "Configuración",
            "downloadAll": "Descargar Todo",
            "clearList": "Limpiar Lista",
            "about": "Acerca de"
        },
        "msg": {
            "savedHistory": "Historial guardado",
            "download_success": "Descarga completada",
            "download_paused": "Descarga pausada",
            "deletedHistory": "Historial eliminado",
            "exit_title": "¿Seguro que desea salir?",
            "exit_text": "¿Estás seguro de que quieres salir? Se cancelarán las descargas en curso.",
            "background_application": "La aplicación continúa ejecutándose en segundo plano."
        },
        "history": {
            "title": "Historial de Media Catcher",
            "label": "Historial de descargas",
            "placeholder": "Aquí verá una lista de todos los elementos descargados.",
            "save": "Generar",
            "delete": "Borrar",
            "delete_question": {
                "title": "Eliminar elemento",
                "text": "¿Está seguro de que quieres eliminar este artículo?"
            }
        },
        "about": {
            "title": "Acerca de",
            "text": f"Media Catcher v{__version__}\n\nDesarrollado por ec25\n\nEsta aplicación te permite administrar y descargar contenido multimedia.\n\nRepositorio: https://github.com/Ec-25/media-catcher"
        },
        "configuration": {
            "titleAPP": "Configuración de Media Catcher",
            "title": "Ajusta tu configuración",
            "path": "Directorio",
            "pathPH": "Ingrese la ruta destino",
            "browse": "Navegar",
            "revert": "Revertir",
            "pathPBError": "Ruta no válida",
            "filename": "Nombre del archivo",
            "filenamePH": "Introduzca el nombre del archivo resultante",
            "max_download": "Descargas máximas",
            "type": "Tipo",
            "quality_video": "Calidad de vídeo",
            "quality_audio": "Calidad de audio",
            "quality_default": "Por defecto",
            "quality_worst": "Menor Peso",
            "quality_highest": "Mejor Calidad",
            "format_video": "Formato de vídeo",
            "format_audio": "Formato de audio",
            "subtitles": "Subtítulos",
            "subtitlesPH": "Introduzca la abreviación del lenguaje (separados por comas)",
            "select_filePH": "seleccionar ARCHIVO",
            "select_filePBError": "Archivo no válido",
            "limit_rate": "Tasa límite",
            "limit_ratePH": "Introduzca la tasa límite (en M=MB/s ó K=KB/s)",
            "limit_ratePBError": "Tasa límite no válida",
            "proxyPH": "Introduzca la URL del proxy",
            "proxyPBError": "URL de proxy no válida",
            "thumbnail": "Miniatura",
            "no_overwrites": "Sin sobrescrituras",
            "metadata": "Metadatos",
            "embed_subtitles": "Incrustar subtítulos",
            "restrict_filename": "Restringir nombre de archivo",
            "no_playlist": "Sin lista de reproducción",
            "download_archive": "Guardar historial de descargas",
            "save": "Guardar",
            "cancel": "Cancelar",
            "saved": "Configuración guardada"
        },
        "errors": {
            "not_found": "No se encontró el archivo de configuración.",
            "dependencies_not_found": "No se encontraron las dependencias necesarias. Por favor, instálalo manualmente.\nPara instalar las dependencias faltantes, ejecuta el siguiente comando:\n",
            "download_dep":  "Error al descargar las dependencias. Por favor, verifica tu conexión a internet e inténtalo de nuevo.",
            "invalid_url": "La URL ingresada no es válida.",
            "download_error": "Error al descargar el contenido multimedia.",
            "extract_info": "Error al extraer información del contenido multimedia.",
            "worker_not_found": "No se encontró el trabajador. Intente descargar nuevamente.",
            "deletedHistoryError": "Error al eliminar el historial",
            "limit_rate": "La tasa límite debe ser un (número)(unidad) válido.",
            "proxy": "La URL del proxy debe ser válida.",
            "no_connection": "No se pudo establecer conexión con el servidor. Por favor, verifica tu conexión a internet e inténtalo de nuevo.",
            "unknown": "Desconocida"

        },
        "elements": {
            "placeHolders": {
                "inputUrl": "URL del contenido multimedia",
                "history": {
                    "status": "Estado",
                    "status_finished": "Finalizado",
                    "status_interrupted": "Interrumpido al",
                    "status_not_initialized": "No iniciado",
                    "title": "Título o URL",
                    "size": "Tamaño",
                    "date": "Fecha"
                }
            },
            "buttons": {
                "add": "Agregar"
            },
            "table_model": {
                "title": "Título o URL",
                "type": "Tipo",
                "quality": "Calidad",
                "duration": "Duración",
                "ext": "Extensión",
                "size": "Tamaño",
                "downloaded": "Descargado",
                "speed": "Velocidad",
                "time_remaining": "Restante",
                "action": "🔽"
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
        "title": f"Media Catcher - v{__version__}",
        "menu": {
            "file": "File",
            "edit": "Edit",
            "language": "Language",
            "downloads": "Downloads",
            "help": "Help",
        },
        "menuActions": {
            "exit": "Exit",
            "switch": "Show/Hide",
            "history": "History",
            "configuration": "Configuration",
            "downloadAll": "Download all",
            "clearList": "Clear List",
            "about": "About"
        },
        "msg": {
            "savedHistory": "History saved",
            "download_success": "Download completed",
            "download_paused": "Download paused",
            "deletedHistory": "History deleted",
            "exit_title": "Are you sure you want to exit?",
            "exit_text": "Are you sure you want to exit? Downloads in progress will be canceled.",
            "background_application": "The application continues to run in the background"

        },
        "history": {
            "title": "Media Catcher History",
            "label": "Download History",
            "placeholder": "Here you will see a list of all downloaded items.",
            "save": "Generate",
            "delete": "Delete",
            "delete_question": {
                "title": "Delete item",
                "text": "Are you sure you want to delete this item?"
            }
        },
        "about": {
            "title": "About",
            "text": f"Media Catcher v{__version__}\n\nDeveloped by ec25\n\nThis application allows you to manage and download multimedia content.\n\nRepository: https://github.com/Ec-25/media-catcher"
        },
        "configuration": {
            "titleAPP": "Media Catcher Configuration",
            "title": "Adjust your Settings",
            "path": "Path",
            "pathPH": "Enter the destination path",
            "browse": "Browse",
            "revert": "Revert",
            "pathPBError": "Invalid path",
            "filename": "Filename",
            "filenamePH": "Enter the filename of the configuration file",
            "max_download": "Max Downloads",
            "type": "Type",
            "quality_video": "Video Quality",
            "quality_audio": "Audio Quality",
            "quality_default": "Default",
            "quality_worst": "Lower Weight",
            "quality_highest": "Better Quality",
            "format_video": "Format Video",
            "format_audio": "Format Audio",
            "subtitles": "Subtitles",
            "subtitlesPH": "Enter the language abbreviation (separated by commas)",
            "select_filePH": "select FILE",
            "select_filePBError": "Invalid file",
            "limit_rate": "Limit Rate",
            "limit_ratePH": "Enter the limit rate (in M=MB/s or K=KB/s)",
            "limit_ratePBError": "Invalid limit rate",
            "proxyPH": "Enter the proxy URL",
            "proxyPBError": "Invalid proxy URL",
            "thumbnail": "Thumbnail",
            "no_overwrites": "No Overwrites",
            "metadata": "Metadata",
            "embed_subtitles": "Embed Subtitles",
            "restrict_filename": "Restrict Filename",
            "no_playlist": "No Playlist",
            "download_archive": "Save download history",
            "save": "Save",
            "cancel": "Cancel",
            "saved": "Configuration saved"
        },
        "errors": {
            "not_found": "Configuration file not found.",
            "dependencies_not_found": "The required dependencies were not found. Please install it manually.\nTo install the missing dependencies, run the following command:\n",
            "download_dep":  "Error downloading dependencies. Please check your internet connection and try again.",
            "invalid_url": "The entered URL is not valid.",
            "download_error": "Error downloading multimedia content.",
            "extract_info": "Error extracting multimedia content information.",
            "worker_not_found": "Worker not found. Try downloading again.",
            "deletedHistoryError": "Error deleting history",
            "limit_rate": "The limit rate must be a valid (number)(unit) valid.",
            "proxy": "The proxy URL must be valid.",
            "no_connection": "The server could not be connected. Please check your internet connection and try again.",
            "unknown": "Unknown"
        },
        "elements": {
            "placeHolders": {
                "inputUrl": "URL of the multimedia content",
                "history": {
                    "status": "Status",
                    "status_finished": "Finished",
                    "status_interrupted": "Interrupted at",
                    "status_not_initialized": "Not initialized",
                    "title": "Title or URL",
                    "size": "Size",
                    "date": "Date"
                }
            },
            "buttons": {
                "add": "Add"
            },
            "table_model": {
                "title": "Title or URL",
                "type": "Type",
                "quality": "Quality",
                "duration": "Duration",
                "ext": "Extension",
                "size": "Size",
                "downloaded": "Downloaded",
                "speed": "Speed",
                "time_remaining": "Remaining",
                "action": "🔽"
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
