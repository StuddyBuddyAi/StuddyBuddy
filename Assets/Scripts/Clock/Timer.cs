using UnityEngine;
using TMPro;

public class TimerController : MonoBehaviour
{
    public TextMeshProUGUI timerDisplay;
    private int totalSeconds = 0;
    private float countdown = 0f;
    private bool isRunning = false;
    private int lastDisplayedSeconds = -1;

    void Update()
    {
        if (isRunning && totalSeconds > 0)
        {
            countdown += Time.deltaTime;

            if (countdown >= 1f)
            {
                int secondsToSubtract = Mathf.FloorToInt(countdown);
                totalSeconds -= secondsToSubtract;
                countdown -= secondsToSubtract;

                if (totalSeconds <= 0)
                {
                    totalSeconds = 0;
                    isRunning = false;
                }

                UpdateDisplay();
            }
        }
    }

    public void AddSeconds(int amount)
    {
        totalSeconds = Mathf.Max(0, totalSeconds + amount);
        UpdateDisplay();
    }

    public void PlayTimer()
    {
        if (!isRunning && totalSeconds > 0)
        {
            isRunning = true;
        }
    }

    public void PauseTimer()
    {
        isRunning = false;
    }

    void UpdateDisplay()
    {
        if (totalSeconds != lastDisplayedSeconds)
        {
            int hours = totalSeconds / 3600;
            int minutes = (totalSeconds % 3600) / 60;
            int seconds = totalSeconds % 60;
            timerDisplay.text = $"{hours:00}:{minutes:00}:{seconds:00}";
            lastDisplayedSeconds = totalSeconds;
        }
    }
}
