import cloudinary
import cloudinary.uploader
import os

def get_cloudinary_config():
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

def upload_image(file, folder="petmatch-solicitudes", public_id=None):
    """
    Sube una imagen a Cloudinary y retorna la URL.
    :param file: archivo tipo bytes o file-like
    :param folder: carpeta en Cloudinary
    :param public_id: nombre personalizado del archivo (sin extensión)
    :return: url de la imagen subida
    """
    get_cloudinary_config()
    upload_params = {"folder": folder}
    if public_id:
        upload_params["public_id"] = public_id
    result = cloudinary.uploader.upload(file, **upload_params)
    return result.get("secure_url")

def delete_image(image_url: str) -> bool:
    """
    Elimina una imagen de Cloudinary
    
    Args:
        image_url (str): URL de la imagen a eliminar
        
    Returns:
        bool: True si se eliminó correctamente, False en caso contrario
    """
    try:
        get_cloudinary_config()
        
        # Extraer public_id de la URL de Cloudinary
        if "cloudinary.com" in image_url:
            # La URL tiene formato: https://res.cloudinary.com/cloud_name/image/upload/v1234567890/folder/filename.jpg
            # Necesitamos extraer: folder/filename (sin extensión)
            parts = image_url.split("/")
            if "upload" in parts:
                upload_index = parts.index("upload")
                if upload_index + 2 < len(parts):
                    # Obtener la parte después de "upload" y antes del último elemento (que es el filename con extensión)
                    path_parts = parts[upload_index + 2:-1]
                    filename = parts[-1]
                    # Remover extensión del filename
                    filename_without_ext = filename.split(".")[0]
                    # Construir public_id
                    public_id = "/".join(path_parts + [filename_without_ext])
                    
                    # Eliminar imagen
                    result = cloudinary.uploader.destroy(public_id)
                    if result.get("result") == "ok":
                        print(f"✅ Imagen eliminada de Cloudinary: {public_id}")
                        return True
                    else:
                        print(f"⚠️ Error eliminando imagen de Cloudinary: {result}")
                        return False
                else:
                    print(f"⚠️ URL de Cloudinary malformada: {image_url}")
                    return False
            else:
                print(f"⚠️ URL no es de Cloudinary: {image_url}")
                return False
        else:
            print(f"⚠️ URL no es de Cloudinary: {image_url}")
            return False
            
    except Exception as e:
        print(f"❌ Error eliminando imagen de Cloudinary: {str(e)}")
        return False