using UnityEngine;
using TMPro;

public class ToggleButton : MonoBehaviour
{
    public Transform targetObject;
    public Transform textObject;

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
    }
}
