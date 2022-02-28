from server_class import *
        
def main():
    try:
        threads = []

        menu_thread = Thread(target=menu)
        threads.append(menu_thread)
        menu_thread.start()

        web_thread = Thread(target=web_task,args=('10.0.0.60',9090))
        threads.append(web_thread)
        web_thread.start()

        server_thread = Thread(target=server_listen,args=('10.0.0.60',12345))
        threads.append(server_thread)
        server_thread.start()
    
        for t in threads:
            t.join()
            
    except KeyboardInterrupt:
        for t in threads:
            t.join()
      
if __name__ == "__main__":
    main()