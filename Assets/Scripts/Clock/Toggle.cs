using UnityEngine;
using TMPro;

public class ToggleButton : MonoBehaviour
{
    public Transform targetObject;
    public Transform textObject;
    public GameObject objectToToggle1;
    public GameObject objectToToggle2;

    public void FlipX()
    {
        
        if (targetObject != null)
        {
            Vector3 scale = targetObject.localScale;
            scale.x *= -1f;
            targetObject.localScale = scale;
        }

        if (textObject != null)
        {
            Vector3 scale = textObject.localScale;
            scale.x *= -1f;
            textObject.localScale = scale;
        }

        
        if (objectToToggle1 != null)
        {
            objectToToggle1.SetActive(!objectToToggle1.activeSelf);
        }

        if (objectToToggle2 != null)
        {
            objectToToggle2.SetActive(!objectToToggle2.activeSelf);
        }
    }
}
