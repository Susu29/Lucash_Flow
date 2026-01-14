def form_valid(self, form):
    selected = form.cleaned_data[self.party_type]
    party_url_field = self.party_type.lower()
    if self.party_type == "Suppliers":
        return redirect("accounting:delete_suppliers", pk=selected.id)
    elif self.party_type == "Customers":
        return redirect("accounting:delete_customers", pk=selected.id)
    
# GOAL = PUT x_x




def form_valid(self, form):
    selected = form.cleaned_data[self.party_type]

    if self.party_type == "Suppliers":
        return redirect("accounting:delete_suppliers", pk=selected.id)
    elif self.party_type == "Customers":
        return redirect("accounting:delete_customers", pk=selected.id)
    