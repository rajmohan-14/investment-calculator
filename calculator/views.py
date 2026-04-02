from django.shortcuts import render

def home(request):
    context = {}

    if request.method == 'POST':

        # Get values from form
        monthly_sip = float(request.POST.get('monthly_sip'))
        lump_sum    = float(request.POST.get('lump_sum'))
        years       = int(request.POST.get('years'))
        annual_rate = float(request.POST.get('annual_rate')) / 100
        inflation   = float(request.POST.get('inflation')) / 100
        stepup_rate = float(request.POST.get('stepup_rate', 0)) / 100
        goal_amount = request.POST.get('goal_amount')

        # SIP Calculation
        r      = annual_rate / 12
        n      = years * 12
        sip_fv = monthly_sip * (((1 + r)**n - 1) / r) * (1 + r)

        # Lump Sum Calculation
        ls_fv = lump_sum * (1 + annual_rate)**years

        # Step-up SIP Calculation
        stepup_corpus = 0
        current_sip   = monthly_sip
        stepup_yearly = []

        for y in range(1, years + 1):
            for m in range(12):
                stepup_corpus = stepup_corpus * (1 + r) + current_sip
            current_sip = current_sip * (1 + stepup_rate)
            stepup_yearly.append(round(stepup_corpus, 2))

        stepup_fv   = round(stepup_corpus, 2)
        stepup_real = round(stepup_corpus / (1 + inflation)**years, 2)

        # Inflation Adjusted Values
        sip_real = round(sip_fv / (1 + inflation)**years, 2)
        ls_real  = round(ls_fv  / (1 + inflation)**years, 2)

        # Year by year data for chart
        years_list = []
        sip_yearly = []
        ls_yearly  = []

        for y in range(1, years + 1):
            n_y   = y * 12
            sip_y = monthly_sip * (((1 + r)**n_y - 1) / r) * (1 + r)
            ls_y  = lump_sum * (1 + annual_rate)**y
            years_list.append(y)
            sip_yearly.append(round(sip_y, 2))
            ls_yearly.append(round(ls_y, 2))

        # Goal Based Calculation
        required_sip = None
        if goal_amount:
            goal_amount  = float(goal_amount)
            required_sip = round(
                goal_amount * r / (((1 + r)**n - 1) * (1 + r)), 2
            )

        context = {
            'sip_fv'        : round(sip_fv, 2),
            'ls_fv'         : round(ls_fv, 2),
            'sip_real'      : sip_real,
            'ls_real'       : ls_real,
            'stepup_fv'     : stepup_fv,
            'stepup_real'   : stepup_real,
            'years_list'    : years_list,
            'sip_yearly'    : sip_yearly,
            'ls_yearly'     : ls_yearly,
            'stepup_yearly' : stepup_yearly,
            'required_sip'  : required_sip,
            'goal_amount'   : goal_amount if goal_amount else '',

            # Repopulate form
            'monthly_sip'   : monthly_sip,
            'lump_sum'      : lump_sum,
            'years'         : years,
            'annual_rate'   : annual_rate * 100,
            'inflation'     : inflation * 100,
            'stepup_rate'   : stepup_rate * 100,
        }

    return render(request, 'calculator/home.html', context)