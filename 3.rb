#encoding: utf-8
require 'sqlite3'

db = SQLite3::Database.new('movies.db')

reviews = db.execute("SELECT distinct word FROM cnt_table WHERE word not like '%''%' GROUP BY word ORDER BY sum(num) desc").flatten

id = 0
reviews.each do |str|
    db.execute("INSERT INTO num_words values(?,?)", id, str)
    id += 1
end

db.close