# https://www.youtube.com/playlist?list=PLqx8fDb-FZDFznZcXb_u_NyiQ7Nai674-
from tkinter import *
from tkinter import ttk
import sqlite3

class Funcs:
    def _clear_screen(self):
        self._entry_codigo.delete(0, 'end')
        self._entry_nome.delete(0, 'end')
        self._entry_telefone.delete(0, 'end')
        self._entry_cidade.delete(0, 'end')

    def _connect(self):
        self._conn = sqlite3.connect('clientes.db'); print('Conectando ao banco de dados')
    
    def _disconnect(self):
        self._conn.close(); print('Desconectando do banco de dados')
    
    def _create_tables(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS tb_clientes (
                codigo INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade VARCHAR(40)
            );
        '''
        self._connect()
        with self._conn as conn:
            conn.execute(sql)
        self._disconnect()
    
    def _get_entry(self):
        self._codigo = self._entry_codigo.get()
        self._nome = self._entry_nome.get()
        self._telefone = self._entry_telefone.get()
        self._cidade = self._entry_cidade.get()
        
    def _add_client(self):
        self._get_entry()
        sql ='''
            INSERT INTO tb_clientes (nome, telefone, cidade)
            VALUES (?, ?, ?);
        '''
        values = (self._nome, self._telefone, self._cidade)
        self._connect()
        with self._conn as conn:
            conn.execute(sql, values)
        self._disconnect()
        self._clear_screen()
        self._select_treeview()
        
    def _select_treeview(self):
        self._treeview.delete(*self._treeview.get_children())
        self._connect()
        sql = 'SELECT codigo, nome, telefone, cidade FROM tb_clientes ORDER BY nome ASC;'
        rows = self._conn.execute(sql).fetchall()
        self._disconnect()
        for row in rows:
            self._treeview.insert('', 'end', values=row)
    
    def _on_doble_click(self, event):
        self._clear_screen()
        print(self._treeview.selection())
        print(event)
        
        for n in self._treeview.selection():
            col1, col2, col3, col4 = self._treeview.item(n, 'values')
            self._entry_codigo.insert('end',col1)
            self._entry_nome.insert('end',col2)
            self._entry_telefone.insert('end',col3)
            self._entry_cidade.insert('end',col4)
    
    def _delete_client(self):
        self._get_entry()
        sql ='''
            DELETE FROM tb_clientes WHERE
            codigo = ?;
        '''
        values = (self._codigo,)
        self._connect()
        with self._conn as conn:
            conn.execute(sql, values); print(f'Cliente com codigo = {self._codigo} foi deletado')
        self._disconnect()
        self._clear_screen()
        self._select_treeview()

    def _update_client(self):
        self._get_entry()
        sql ='''
            UPDATE tb_clientes SET nome = ?, telefone = ?, cidade = ?
            WHERE codigo = ?;
        '''
        values = (self._nome, self._telefone, self._cidade, self._codigo)
        self._connect()
        with self._conn as conn:
            conn.execute(sql, values)
        self._disconnect()
        self._clear_screen()
        self._select_treeview()
        
   
class App(Funcs):
    def __init__(self, root) -> None:
        self._root = root
        self._colors = {
            'white':'#FFFFFF',
            'darkblue':'#1E3743',
            'lightblue':'#759FE6',
            'blue':'#107DB2',
            'gray':'#DFE3EE'
        }
        self._font_1 = ('verdana', 8, 'bold')
        self._tela()
        self._frames_da_tela()
        self._widgets_frame_1()
        self._widgets_frame_2()
        self._create_tables()
        self._select_treeview()
        self._root.mainloop()
    
    def _tela(self):
        self._root.title('Cadastro de Clientes')
        self._root.configure(background=self._colors['darkblue'])
        self._root.geometry('700x500')
        self._root.resizable(True, True)
        self._root.maxsize(width=900, height=700)
        self._root.minsize(width=500, height=400)

    def _frames_da_tela(self):
        self._frame_1 = Frame(self._root, border=4, background=self._colors['gray'],
                              highlightbackground=self._colors['lightblue'], highlightthickness=3)
        self._frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        
        self._frame_2 = Frame(self._root, border=4, background=self._colors['gray'],
                              highlightbackground=self._colors['lightblue'], highlightthickness=3)
        self._frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def _widgets_frame_1(self):
        # Criação do botão limpar
        self._bt_limpar = Button(self._frame_1, text='Limpar', border=2, background=self._colors['blue'],
                                foreground=self._colors['white'], font=self._font_1, command=self._clear_screen)
        self._bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
        
        # Criação do botão buscar
        self._bt_buscar = Button(self._frame_1, text='Buscar', border=2, background=self._colors['blue'],
                                foreground=self._colors['white'], font=self._font_1)
        self._bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        
        # Criação do botão novo
        self._bt_novo = Button(self._frame_1, text='Novo', border=2, background=self._colors['blue'],
                                foreground=self._colors['white'], font=self._font_1, command=self._add_client)
        self._bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        
        # Criação do botão alterar
        self._bt_alterar = Button(self._frame_1, text='Alterar', border=2, background=self._colors['blue'],
                                foreground=self._colors['white'], font=self._font_1, command=self._update_client)
        self._bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        
        # Criação do botão apagar
        self._bt_apagar = Button(self._frame_1, text='Apagar', border=2, background=self._colors['blue'],
                                foreground=self._colors['white'], font=self._font_1, command=self._delete_client)
        self._bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        
        #Criação da label codigo
        self._lb_codigo = Label(
                                    self._frame_1,
                                    text='Código',
                                    border=2,
                                    background=self._colors['gray'],
                                    foreground=self._colors['blue']
                                )
        self._lb_codigo.place(relx=0.05, rely=0.05)
        
        #Criação da entrada codigo
        self._entry_codigo = Entry(self._frame_1)
        self._entry_codigo.place(relx=0.05, rely=0.15, relwidth=0.08)
        
        #Criação da label nome
        self._lb_nome = Label(self._frame_1, text='Nome', background=self._colors['gray'],
                              foreground=self._colors['blue'])
        self._lb_nome.place(relx=0.05, rely=0.35)
        
        #Criação da entrada nome
        self._entry_nome = Entry(self._frame_1)
        self._entry_nome.place(relx=0.05, rely=0.45, relwidth=0.8)
        
        #Criação da label telefone
        self._lb_telefone = Label(self._frame_1, text='Telefone', background=self._colors['gray'],
                                  foreground=self._colors['blue'])
        self._lb_telefone.place(relx=0.05, rely=0.6)
        
        #Criação da entrada telefone
        self._entry_telefone = Entry(self._frame_1)
        self._entry_telefone.place(relx=0.05, rely=0.7, relwidth=0.4)
        
        #Criação da label cidade
        self._lb_cidade = Label(self._frame_1, text='Cidade', background=self._colors['gray'],
                                foreground=self._colors['blue'])
        self._lb_cidade.place(relx=0.5, rely=0.6)
        
        #Criação da entrada cidade
        self._entry_cidade = Entry(self._frame_1)
        self._entry_cidade.place(relx=0.5, rely=0.7, relwidth=0.4)
    
    def _widgets_frame_2(self):
        self._treeview = ttk.Treeview(self._frame_2, height=3, columns=('col1', 'col2', 'col3', 'col4'), show='headings')
        self._treeview.heading(column='#0', text='')
        self._treeview.heading(column='#1', text='Codigo')
        self._treeview.heading(column='#2', text='Nome')
        self._treeview.heading(column='#3', text='Telefone')
        self._treeview.heading(column='#4', text='Cidade')
        
        self._treeview.column(column='#0', width=1)
        self._treeview.column(column='#1', width=50)
        self._treeview.column(column='#2', width=200)
        self._treeview.column(column='#3', width=125)
        self._treeview.column(column='#4', width=125)
        
        self._treeview.place(relx=0.01, rely=0.01, relwidth=0.95, relheight=0.85)
        
        self._scroolbar = ttk.Scrollbar(self._frame_2, orient='vertical')
        self._treeview.configure(yscrollcommand=self._scroolbar.set)
        self._scroolbar.place(relx=0.96, rely=0.01, relwidth=0.04, relheight=0.85)
        self._treeview.bind('<Double-1>', self._on_doble_click)
        

if __name__ == '__main__':
    root = Tk()
    App(root)