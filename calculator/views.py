from django.shortcuts import render

def home(request):
    context = {}

    if request.method == 'POST':

        monthly_sip = float(request.POST.get('monthly_sip'))
        lump_sum    = float(request.POST.get('lump_sum'))
        years       = int(request.POST.get('years'))
        annual_rate = float(request.POST.get('annual_rate')) / 100
        inflation   = float(request.POST.get('inflation')) / 100

        r   = annual_rate / 12        # monthly rate
        n   = years * 12              # total months
        sip_fv = monthly_sip * (((1 + r)**n - 1) / r) * (1 + r)

        # Step 3 - Lump Sum Calculation
        ls_fv = lump_sum * (1 + annual_rate)**years

        # Step 4 - Inflation Adjusted Real Values
        sip_real = sip_fv / (1 + inflation)**years
        ls_real  = ls_fv  / (1 + inflation)**years

        # Step 5 - Send results to template
        context = {
            'sip_fv'   : round(sip_fv, 2),
            'ls_fv'    : round(ls_fv, 2),
            'sip_real' : round(sip_real, 2),
            'ls_real'  : round(ls_real, 2),

            # Send form values back so fields don't empty after submit
            'monthly_sip' : monthly_sip,
            'lump_sum'    : lump_sum,
            'years'       : years,
            'annual_rate' : annual_rate * 100,
            'inflation'   : inflation * 100,
        }

    return render(request, 'calculator/home.html', context)