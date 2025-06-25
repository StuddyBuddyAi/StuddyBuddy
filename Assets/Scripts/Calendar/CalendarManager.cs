using System;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class CalendarManager : MonoBehaviour
{
    public TextMeshProUGUI monthLabel;
    public TextMeshProUGUI selectedDateLabel;
    public Button prevButton;
    public Button nextButton;
    public GameObject dayCellPrefab;
    public Transform dayGrid;

    public TMP_InputField noteInputField;
    public TextMeshProUGUI noteDisplayText;
    public Button saveNoteButton;
    public Button clearNoteButton; // Optional

    private DateTime currentDate;
    private int todayDay;
    private bool clickedTodayThisMonth = false;
    private string currentDateKey;

    void Start()
    {
        currentDate = DateTime.Now;
        todayDay = currentDate.Day;
        GenerateCalendar(currentDate.Year, currentDate.Month);

        prevButton.onClick.AddListener(() => ChangeMonth(-1));
        nextButton.onClick.AddListener(() => ChangeMonth(1));
        saveNoteButton.onClick.AddListener(SaveNote);
        clearNoteButton?.onClick.AddListener(ClearNote);
    }

    void ChangeMonth(int offset)
    {
        currentDate = currentDate.AddMonths(offset);
        GenerateCalendar(currentDate.Year, currentDate.Month);
    }

    void GenerateCalendar(int year, int month)
    {
        monthLabel.text = $"{year}\n{new DateTime(year, month, 1):MMMM}";
        clickedTodayThisMonth = false;

        foreach (Transform child in dayGrid)
            Destroy(child.gameObject);

        int daysInMonth = DateTime.DaysInMonth(year, month);
        int startDay = (int)new DateTime(year, month, 1).DayOfWeek;

        for (int i = 0; i < startDay; i++)
        {
            GameObject blankCell = Instantiate(dayCellPrefab, dayGrid);
            var img = blankCell.GetComponent<Image>();
            if (img) img.color = new Color(0, 0, 0, 0);
        }

        for (int day = 1; day <= daysInMonth; day++)
        {
            GameObject cell = Instantiate(dayCellPrefab, dayGrid);
            TextMeshProUGUI dayText = cell.GetComponentInChildren<TextMeshProUGUI>();
            dayText.text = day.ToString();

            int capturedDay = day;
            cell.GetComponent<Button>().onClick.AddListener(() => OnDayClicked(capturedDay));

            // Highlight today
            if (year == DateTime.Now.Year && month == DateTime.Now.Month && day == DateTime.Now.Day)
            {
                cell.GetComponent<Image>().color = new Color(1f, 0.9f, 0.6f);

                if (!clickedTodayThisMonth)
                {
                    OnDayClicked(capturedDay);
                    clickedTodayThisMonth = true;
                }
            }
        }
    }

    void OnDayClicked(int day)
    {
        DateTime clickedDate = new DateTime(currentDate.Year, currentDate.Month, day);
        currentDateKey = clickedDate.ToString("yyyy-MM-dd");

        string formattedDate = $"{clickedDate:dddd MMMM} {GetDayWithSuffix(day)} {clickedDate:yyyy}";
        selectedDateLabel.text = formattedDate;

        string savedNote = PlayerPrefs.GetString(currentDateKey, "");
        noteInputField.text = savedNote;
        noteDisplayText.text = string.IsNullOrWhiteSpace(savedNote) ? "(Add a New Note)" : savedNote;
    }

    void SaveNote()
    {
        if (!string.IsNullOrEmpty(currentDateKey))
        {
            string note = noteInputField.text;
            PlayerPrefs.SetString(currentDateKey, note);
            noteDisplayText.text = string.IsNullOrWhiteSpace(note) ? "(Add a New Note)" : note;
        }
    }

    void ClearNote()
    {
        if (!string.IsNullOrEmpty(currentDateKey))
        {
            PlayerPrefs.DeleteKey(currentDateKey);
            noteInputField.text = "";
            noteDisplayText.text = "(Add a New Note)";
        }
    }

    string GetDayWithSuffix(int day)
    {
        if (day >= 11 && day <= 13) return day + "th";

        switch (day % 10)
        {
            case 1: return day + "st";
            case 2: return day + "nd";
            case 3: return day + "rd";
            default: return day + "th";
        }
    }
}
