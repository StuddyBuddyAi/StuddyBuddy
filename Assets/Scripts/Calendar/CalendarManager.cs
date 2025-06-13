using System;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class CalendarManager : MonoBehaviour
{
    public TextMeshProUGUI monthLabel;
    public Button prevButton;
    public Button nextButton;
    public GameObject dayCellPrefab;
    public Transform dayGrid;

    private DateTime currentDate;

    void Start()
    {
        currentDate = DateTime.Now;
        GenerateCalendar(currentDate.Year, currentDate.Month);

        prevButton.onClick.AddListener(() => ChangeMonth(-1));
        nextButton.onClick.AddListener(() => ChangeMonth(1));
    }

    void ChangeMonth(int offset)
    {
        currentDate = currentDate.AddMonths(offset);
        GenerateCalendar(currentDate.Year, currentDate.Month);
    }

    void GenerateCalendar(int year, int month)
    {
        monthLabel.text = $"{year}\n{new DateTime(year, month, 1).ToString("MMMM")}";


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

            if (year == DateTime.Now.Year && month == DateTime.Now.Month && day == DateTime.Now.Day)
                cell.GetComponent<Image>().color = new Color(1f, 0.9f, 0.6f);
        }
    }
}
