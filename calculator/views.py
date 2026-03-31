from django.shortcuts import render

def home(request):
    context = {}

    if request.method == 'POST':

        # Step 1 - Get values from the form
        monthly_sip = float(request.POST.get('monthly_sip'))
        lump_sum    = float(request.POST.get('lump_sum'))
        years       = int(request.POST.get('years'))
        annual_rate = float(request.POST.get('annual_rate')) / 100
        inflation   = float(request.POST.get('inflation')) / 100

        # Step 2 - SIP Calculation
        r      = annual_rate / 12
        n      = years * 12
        sip_fv = monthly_sip * (((1 + r)**n - 1) / r) * (1 + r)

        # Step 3 - Lump Sum Calculation
        ls_fv = lump_sum * (1 + annual_rate)**years

        # Step 4 - Inflation Adjusted Real Values
        sip_real = sip_fv / (1 + inflation)**years
        ls_real  = ls_fv  / (1 + inflation)**years

        # Step 5 - Year by year data for chart
        years_list  = []
        sip_yearly  = []
        ls_yearly   = []

        for y in range(1, years + 1):
            n_y   = y * 12
            sip_y = monthly_sip * (((1 + r)**n_y - 1) / r) * (1 + r)
            ls_y  = lump_sum * (1 + annual_rate)**y

            years_list.append(y)
            sip_yearly.append(round(sip_y, 2))
            ls_yearly.append(round(ls_y, 2))

        # Step 6 - Send results to template
        context = {
            'sip_fv'     : round(sip_fv, 2),
            'ls_fv'      : round(ls_fv, 2),
            'sip_real'   : round(sip_real, 2),
            'ls_real'    : round(ls_real, 2),
            'years_list' : years_list,
            'sip_yearly' : sip_yearly,
            'ls_yearly'  : ls_yearly,

            # Repopulate form fields
            'monthly_sip' : monthly_sip,
            'lump_sum'    : lump_sum,
            'years'       : years,
            'annual_rate' : annual_rate * 100,
            'inflation'   : inflation * 100,
        }

    return render(request, 'calculator/home.html', context)