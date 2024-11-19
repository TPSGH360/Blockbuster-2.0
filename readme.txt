SU:
TPS
avrumidoh@gmail.com
pdnejoh420

registers:
1.  samana
    lxgiwyl360

2.  kira
    aiypdzqp240

3.  customer_1
    lxgiwyl420

4.  customer_2
    aiypdzqp550

5.  customer_3
    jaezakmi880

6.  customer_4
    jaezakmi420





# def home(request):
#     display_edit = request.user.is_authenticated and request.user.is_staff
#     return render(request, "movies/index.html", {"display_edit": display_edit})


{% extends "movies/main.html" %} {% block content %}
<h1 class="mb-4">Loans</h1>
<div id="loan-list" class="row"></div>

<script>
  async function fetchLoans() {
    try {
      const response = await axios.get("/api/loans/");
      const loans = response.data;

      const loanList = document.getElementById("loan-list");
      loans.forEach((loan) => {
        const loanCard = `
                    <div class="col-md-4 mb-3">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Loan by: ${
                                  loan.customer
                                }</h5>
                                <p class="card-text">Movie: ${
                                  loan.movie.title
                                }</p>
                                <p class="card-text">Loan Date: ${
                                  loan.loan_date
                                }</p>
                                <p class="card-text">Return Date: ${
                                  loan.return_date || "Not returned"
                                }</p>
                                <p class="card-text">Status: ${
                                  loan.is_active ? "Active" : "Completed"
                                }</p>
                            </div>
                        </div>
                    </div>`;
        loanList.innerHTML += loanCard;
      });
    } catch (error) {
      console.error("Error fetching loans:", error);
    }
  }

  fetchLoans();
</script>
{% endblock %}
