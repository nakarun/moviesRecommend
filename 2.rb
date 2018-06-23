#encoding: utf-8
require 'csv'
require 'natto'
require 'sqlite3'

db = SQLite3::Database.new('movies.db')

#create table to insert words cut by natto
#db.execute("CREATE TABLE words(
#		id int primary key,
#		title varchar(30),
#		words varchar(30),
#		num int
#	   )")


reviews = db.execute("SELECT * FROM reviews")

       reviews.each do |str|

           id = str[0]
           title = str[1]
           text = str[2]

           nm = Natto::MeCab.new

           nm.parse(text) do |n|
               db.execute("INSERT INTO cnt_table values(?,?,?,?)", id, title, n.surface, 1)
           end

        end


db.close
