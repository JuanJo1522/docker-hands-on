db = db.getSiblingDB('movies_db');

const movies = [
  { title: 'The Shawshank Redemption', category: 'drama', year: 1994, synopsis: 'Two men find hope and friendship while serving life sentences.' },
  { title: 'Pulp Fiction', category: 'drama', year: 1994, synopsis: 'Interconnected stories unfold in the Los Angeles underworld.' },
  { title: 'Forrest Gump', category: 'drama', year: 1994, synopsis: 'A kind-hearted man witnesses defining moments in American history.' },
  { title: 'The Godfather', category: 'drama', year: 1972, synopsis: 'The aging patriarch of a crime family transfers control to his son.' },
  { title: 'Good Will Hunting', category: 'drama', year: 1997, synopsis: 'A gifted janitor finds direction with help from a therapist.' },
  { title: 'The Green Mile', category: 'drama', year: 1999, synopsis: 'A death-row guard encounters a prisoner with a mysterious gift.' },
  { title: 'The Truman Show', category: 'drama', year: 1998, synopsis: 'A man discovers that his life may be a television production.' },
  { title: 'Whiplash', category: 'drama', year: 2014, synopsis: 'A young drummer faces the demanding teaching style of a conductor.' },
  { title: 'Superbad', category: 'comedy', year: 2007, synopsis: 'Two friends try to make the most of their final days of high school.' },
  { title: 'The Hangover', category: 'comedy', year: 2009, synopsis: 'Friends retrace a wild night in Las Vegas before a wedding.' },
  { title: 'Groundhog Day', category: 'comedy', year: 1993, synopsis: 'A cynical weatherman relives the same day again and again.' },
  { title: 'School of Rock', category: 'comedy', year: 2003, synopsis: 'A musician turns a classroom into a rock band.' },
  { title: 'Mean Girls', category: 'comedy', year: 2004, synopsis: 'A new student navigates the social rules of high school.' },
  { title: 'The Grand Budapest Hotel', category: 'comedy', year: 2014, synopsis: 'A hotel concierge and his protégé become involved in a grand adventure.' },
  { title: 'Little Miss Sunshine', category: 'comedy', year: 2006, synopsis: 'A family takes an eventful road trip to a children’s pageant.' },
  { title: 'Paddington 2', category: 'comedy', year: 2017, synopsis: 'Paddington tries to clear his name after a special book is stolen.' },
  { title: 'The Dark Knight', category: 'thriller', year: 2008, synopsis: 'Batman faces a criminal mastermind who throws Gotham into chaos.' },
  { title: 'Se7en', category: 'thriller', year: 1995, synopsis: 'Two detectives pursue a killer whose crimes follow the seven deadly sins.' },
  { title: 'The Silence of the Lambs', category: 'thriller', year: 1991, synopsis: 'An FBI trainee seeks insight from an imprisoned serial killer.' },
  { title: 'Shutter Island', category: 'thriller', year: 2010, synopsis: 'A marshal investigates the disappearance of a patient from an island hospital.' },
  { title: 'Gone Girl', category: 'thriller', year: 2014, synopsis: 'A husband becomes the focus of suspicion when his wife disappears.' },
  { title: 'Get Out', category: 'thriller', year: 2017, synopsis: 'A weekend visit uncovers unsettling secrets about a family.' },
  { title: 'Prisoners', category: 'thriller', year: 2013, synopsis: 'A desperate father searches for his missing daughter.' },
  { title: 'Knives Out', category: 'thriller', year: 2019, synopsis: 'A detective investigates the death of a wealthy mystery writer.' },
];

for (const movie of movies) {
  db.movies.updateOne({ title: movie.title }, { $set: movie }, { upsert: true });
}
