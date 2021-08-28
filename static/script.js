document.addEventListener('DOMContentLoaded', function() {
    let interval = document.querySelectorAll('.remaining_days');
    for (let i=0; i<interval.length; i++)
    {
        let number = interval[i].innerHTML;
        if (number === '1')
        {
            interval[i].style.color = 'red';
        }
        else if (number === '2')
        {
            interval[i].style.color = '#FFA500';
        }
        else if (number === '3')
        {
            interval[i].style.color = '#FFC0CB';
        }
    }
});