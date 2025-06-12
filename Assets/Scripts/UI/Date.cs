using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class Date : MonoBehaviour
{

    public TextMeshProUGUI largeText;

    void Start()
    {

        string date = System.DateTime.UtcNow.ToLocalTime().ToString("ddd, MMM dd, yyyy");
        print(date);
        largeText.text = date;

    }
   
}
