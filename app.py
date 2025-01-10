from flask import Flask, render_template, request, redirect, url_for

class Voter:
    def __init__(self, voter_id, name):
        self.voter_id = voter_id
        self.name = name
        self.has_voted = False

    def __repr__(self):
        return f"Voter({self.voter_id}, {self.name}, has_voted={self.has_voted})"


class Candidate:
    def __init__(self, candidate_id, name):
        self.candidate_id = candidate_id
        self.name = name
        self.votes = 0

    def __repr__(self):
        return f"Candidate({self.candidate_id}, {self.name}, votes={self.votes})"


class VotingSystem:
    def __init__(self):
        self.voters = {}
        self.candidates = {}
        self.logs = []

    def register_voter(self, voter_id, name):
        if voter_id in self.voters:
            return f"Voter ID {voter_id} already exists."
        else:
            self.voters[voter_id] = Voter(voter_id, name)
            return f"Voter {name} registered successfully."
        
    def register_candidate(self, candidate_id, name):
    # Check if the voter ID exists
        if candidate_id not in self.voters:
            return f"Invalid Voter ID: {candidate_id}. Only registered voters can be candidates."
    
    # Validate if the voter name matches
        voter = self.voters[candidate_id]
        if voter.name != name:
            return f"Voter ID {candidate_id} and name '{name}' do not match the registered voter details."
    
    # Check if the ID is already registered as a candidate
        if candidate_id in self.candidates:
            return f"Candidate ID {candidate_id} already exists."
    
    # Register the candidate
        self.candidates[candidate_id] = Candidate(candidate_id, name)
        return f"Candidate {name} registered successfully."


    def cast_vote(self, voter_id, candidate_id):
        if voter_id not in self.voters:
            return f"Voter ID {voter_id} not found."

        if candidate_id not in self.candidates:
            return f"Candidate ID {candidate_id} not found."

        voter = self.voters[voter_id]
        if voter.has_voted:
            return f"Voter {voter.name} has already voted."
        else:
            voter.has_voted = True
            self.candidates[candidate_id].votes += 1
            self.logs.append(f"Voter {voter.name} voted for {self.candidates[candidate_id].name}.")
            return f"Vote cast successfully by {voter.name} for {self.candidates[candidate_id].name}."

    def display_results(self):
        return {candidate.name: candidate.votes for candidate in self.candidates.values()}

    def display_logs(self):
        return self.logs



# Flask App
app = Flask(__name__)
system = VotingSystem()

# List of voter names (79 unique names)
voter_names = [
    "PRANAV UMESH", "PATEL NITI", "VAIBAV JAISWAL", "KARAN VAGHELA", "ASHISH JOHN", "PREETAM REDDY", "VADLA VAMSI KRISHNA", "SATHVIKA", "AJAY KUMAR", "GANESH REDDY",
    "SHIVRAJ", "SHREYASH PRADIPBHAI", "JASWANTH", "SUNIDHI SINGH", "SAHIL SAILESH", "CHANDRASEKHAR REDDY", "HARSHAL", "ABHNAY KUMAR", "MURALI", "SRIRAM",
    "VASANTH KUMAR REDDY", "HARSH", "MANIKANTA REDDY", "ADITYA PRAKASH", "HARSH CHAVDA", "DHRUV KUMAR", "BHARATH KALYAN", "VENKATA KISHORE", "MADHU BABU", "SANDHYA",
    "KARTHIKEYA REDDY", "MANJUNATH", "MADHU PRASAD", "VISHNU VARDHAN REDDY", "ABHINASH", "SAI VARDHAN REDDY", "DEVSHRI", "MEGHRAI", "SIDDHARDHA", "NEHA",
    "NARESH", "SAMUYELU", "PRATHMESH", "YATHEESH RAJA", "VINIT KUMAR", "RAFI VALI", "RAMAN RAVINDRA", "BHARGAV", "JEEVAN KUMAR", "UZMAA AFRIN","SRUTHI","SPOORTHIKA","ADITHYA VINOD",
    "ROHITHA","CHARAN KUMAR REDDY","GRESHMANTH","VAMSI KRISHNA","CHARAN SAI","VENU","LAVANYA","PRAVEEN REDDY","YOGI","VARSHINI","SANKET",
    "SAI PRAPUL","GOPI MAHITH","SOMANATH","KAMAL","DHARMATEJA","RUSHIKESH","ANIL NAYAK","SRI SHANTH","VISHNU VARDHAN CHOWDARY","BHARGAV","VIGNESH","HAVISH","TRINADH SAI",
    "KRINAL","NAVYANTH"
]

# Adding 79 voters to the system with the specified names
for i, name in enumerate(voter_names, start=1):
    system.register_voter(i, name)

# Selecting 5 voters to be candidates and registering them as candidates
candidate_ids = [1,3,7,11,29]
for candidate_id in candidate_ids:
    voter = system.voters[candidate_id]
    system.register_candidate(candidate_id, voter.name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_voter', methods=['GET', 'POST'])
def register_voter():
    if request.method == 'POST':
        voter_id = int(request.form['voter_id'])
        name = request.form['name']
        message = system.register_voter(voter_id, name)
        return render_template('register_voter.html', message=message)
    return render_template('register_voter.html')

@app.route('/register_candidate', methods=['GET', 'POST'])
def register_candidate():
    if request.method == 'POST':
        candidate_id = int(request.form['candidate_id'])
        name = request.form['name']
        message = system.register_candidate(candidate_id, name)
        return render_template('register_candidate.html', message=message)
    return render_template('register_candidate.html')

@app.route('/cast_vote', methods=['GET', 'POST'])
def cast_vote():
    if request.method == 'POST':
        voter_id = int(request.form['voter_id'])
        candidate_id = int(request.form['candidate_id'])
        message = system.cast_vote(voter_id, candidate_id)
        return render_template('cast_vote.html', message=message, candidates=system.candidates.values())
    return render_template('cast_vote.html', candidates=system.candidates.values())

@app.route('/results')
def results():
    results = system.display_results()
    return render_template('results.html', results=results)

@app.route('/logs')
def logs():
    logs = system.display_logs()
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)

