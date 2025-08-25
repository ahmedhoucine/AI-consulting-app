class Dashboard:
    def __init__(self, title):
        self.title = title
        self.offre_count = 0
        self.success_rate = 0.0
        self.consultant_status = {}
        self.top_jobs = []
        self.top_skills = []
        self.top_secteurs = []
        self.top_entreprises = []
        self.bottom_entreprises = []
        self.offres_par_localisation=[]

    def to_dict(self):
        return {
            'title': self.title,
            'offre_count': self.offre_count,
            'success_rate': self.success_rate,
            'consultant_status': self.consultant_status,
            'top_jobs': self.top_jobs,
            'top_skills': self.top_skills,
            'top_secteurs': self.top_secteurs,
            'top_entreprises': self.top_entreprises,
            'bottom_entreprises': self.bottom_entreprises,
            "offres_par_localisation":self.offres_par_localisation
        }
