using UnityEngine;

public class InventoryToggle : MonoBehaviour
{
    public GameObject UIPanel;

    public void ToggleInventory()
    {
        Debug.Log("Inventory toggle button clicked.");

        if (UIPanel != null)
        {
            UIPanel.SetActive(!UIPanel.activeSelf);
        }
    }
}
