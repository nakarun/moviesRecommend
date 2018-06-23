require 'nokogiri'
require 'anemone'
require 'sqlite3'

db = SQLite3::Database.new('movies.db')

opts = {
	depth_limit: 1,
    :delay => 5,
}

id = 1

    for num in 10..100 do

        url = "http://www.jtnews.jp/cgi-bin/review.cgi?TITLE_NO=" + num.to_s

        Anemone.crawl( url , opts) do |anemone|
        
            anemone.focus_crawl do |page|
                page.links.keep_if{|link| link.to_s.match(/PAGE_NO=[^1]/)}
            end
        
            i = 1 #page number
            anemone.on_pages_like(//) do |page|
                
                print "PAGE_NO=" + i.to_s + "/ "
         
                title = page.doc.xpath("/html/body//h1//span[@itemprop='name']/text()").to_s
                
                roop = 1
                
                page.doc.xpath("/html/body//table[@class='REV_MAIN_DATA']").each do |node|
                
                    sleep(3)
  
                    until roop == 21 do
                    
                        if node.xpath("./tr[" + roop.to_s + "]/td/div//text()").to_s == ""
                            break
                        end
                    
                        print roop.to_s + ", "
                
                        review = node.xpath("./tr[" + roop.to_s + "]/td/div//text()").to_s
                    
                        db.execute("INSERT INTO reviews values (?, ?, ?)", id, title, review)

                        id += 1
                        roop += 1
                    end
                puts ""
                end
            i += 1
            end
                
            anemone.on_every_page do |page|
                print "TITLE_NO=" + num.to_s + "/ "
            end
        end
    end

db.close
