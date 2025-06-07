using UnityEngine;

public class UIToggle : MonoBehaviour
{
    public GameObject UIPanel;

    public void ToggleUI()
    {

        if (UIPanel != null)
        {
            UIPanel.SetActive(!UIPanel.activeSelf);
        }
    }
}
