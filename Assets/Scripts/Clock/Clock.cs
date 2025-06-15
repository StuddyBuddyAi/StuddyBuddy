using UnityEngine;
using TMPro;
using System;

public class LiveClock : MonoBehaviour
{
    public TextMeshProUGUI timeText;
    private float timer;

    void Update()
    {
        timer += Time.deltaTime;
        if (timer >= 1f)
        {
            timeText.text = DateTime.Now.ToString("HH:mm:ss");
            timer = 0f;
        }
    }
}
