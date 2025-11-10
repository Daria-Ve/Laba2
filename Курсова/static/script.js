function getRecommendations() {
    //Отримуємо значення вибраних трибутів
    const genre = document.getElementById("genre").value;
    const period = document.getElementById("period").value;
    const countries = Array.from(document.querySelectorAll('input[name="country"]:checked')).map(cb => cb.value);
    const resultsDiv = document.getElementById("results");

    fetch("/recommend", { //Надсилаємо POST-запит із параметрами до сервера
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ genre: genre, period: period, countries: countries })
    })
    .then(response => { //Перевірка на помилку відповіді
        if (!response.ok) throw new Error("Сервер не відповідає");
        return response.json();
    })
    .then(data => { // Якщо є рекомендації, створюємо список і додаємо книги
        resultsDiv.innerHTML = "";
        if (data.recommendations?.length > 0) {
            const ul = document.createElement("ul");
            data.recommendations.forEach(book => {
                const li = document.createElement("li");
                li.textContent = `"${book.title}" ${book.author}`;
                ul.appendChild(li);
            });
            resultsDiv.appendChild(ul);
        } else { // Якщо немає рекомендацій — виводимо повідомлення
            resultsDiv.textContent = "Немає рекомендацій за цими критеріями 😔";
        }
    })
    .catch(error => {
        console.error("Помилка при запиті:", error);
        resultsDiv.textContent = "Сталася помилка. Спробуйте ще раз.";
    });
}
