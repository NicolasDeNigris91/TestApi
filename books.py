from fastapi import FastAPI, Body, Query
from typing import Optional  # Importe Optional para parâmetros opcionais

app = FastAPI()

# Lista de clubes e seus melhores jogadores (1990-2010)
CLUBS = [
    {
        "name": "Manchester United",
        "players": [
            {"name": "Eric Cantona", "position": "Forward", "years": "1992-1997"},
            {"name": "Roy Keane", "position": "Midfielder", "years": "1993-2005"},
            {"name": "Ryan Giggs", "position": "Midfielder", "years": "1990-2014"},
            {"name": "Paul Scholes", "position": "Midfielder", "years": "1994-2013"},
            {"name": "David Beckham", "position": "Midfielder", "years": "1995-2003"},
            {"name": "Gary Neville", "position": "Defender", "years": "1992-2011"},
            {"name": "Rio Ferdinand", "position": "Defender", "years": "2002-2014"},
            {"name": "Nemanja Vidić", "position": "Defender", "years": "2006-2014"},
            {"name": "Peter Schmeichel", "position": "Goalkeeper", "years": "1991-1999"},
            {"name": "Ole Gunnar Solskjær", "position": "Forward", "years": "1996-2007"},
            {"name": "Wayne Rooney", "position": "Forward", "years": "2004-2017"}
        ]
    },
    {
        "name": "Real Madrid",
        "players": [
            {"name": "Zinedine Zidane", "position": "Midfielder", "years": "2001-2006"},
            {"name": "Raúl", "position": "Forward", "years": "1994-2010"},
            {"name": "Roberto Carlos", "position": "Defender", "years": "1996-2007"},
            {"name": "Ronaldo Nazário", "position": "Forward", "years": "2002-2007"},
            {"name": "Iker Casillas", "position": "Goalkeeper", "years": "1999-2015"},
            {"name": "Fernando Hierro", "position": "Defender", "years": "1989-2003"},
            {"name": "Claude Makélélé", "position": "Midfielder", "years": "2000-2003"},
            {"name": "Luís Figo", "position": "Midfielder", "years": "2000-2005"},
            {"name": "David Beckham", "position": "Midfielder", "years": "2003-2007"},
            {"name": "Sergio Ramos", "position": "Defender", "years": "2005-2021"},
            {"name": "Guti", "position": "Midfielder", "years": "1995-2010"}
        ]
    },
    {
        "name": "Juventus",
        "players": [
            {"name": "Alessandro Del Piero", "position": "Forward", "years": "1993-2012"},
            {"name": "Gianluigi Buffon", "position": "Goalkeeper", "years": "2001-2018"},
            {"name": "Pavel Nedvěd", "position": "Midfielder", "years": "2001-2009"},
            {"name": "Zinedine Zidane", "position": "Midfielder", "years": "1996-2001"},
            {"name": "Lilian Thuram", "position": "Defender", "years": "2001-2006"},
            {"name": "Edgar Davids", "position": "Midfielder", "years": "1997-2004"},
            {"name": "Alessandro Nesta", "position": "Defender", "years": "1993-2002"},
            {"name": "Filippo Inzaghi", "position": "Forward", "years": "1997-2012"},
            {"name": "Ciro Ferrara", "position": "Defender", "years": "1994-2005"},
            {"name": "Gianluca Zambrotta", "position": "Defender", "years": "1999-2006"},
            {"name": "David Trezeguet", "position": "Forward", "years": "2000-2010"}
        ]
    },
    {
        "name": "Milan",
        "players": [
            {"name": "Paolo Maldini", "position": "Defender", "years": "1985-2009"},
            {"name": "Franco Baresi", "position": "Defender", "years": "1977-1997"},
            {"name": "Andriy Shevchenko", "position": "Forward", "years": "1999-2006, 2008-2009"},
            {"name": "Kaká", "position": "Midfielder", "years": "2003-2009, 2013-2014"},
            {"name": "Clarence Seedorf", "position": "Midfielder", "years": "2002-2012"},
            {"name": "Andrea Pirlo", "position": "Midfielder", "years": "2001-2011"},
            {"name": "Gennaro Gattuso", "position": "Midfielder", "years": "1999-2012"},
            {"name": "Alessandro Costacurta", "position": "Defender", "years": "1987-2007"},
            {"name": "Filippo Inzaghi", "position": "Forward", "years": "2001-2012"},
            {"name": "Dida", "position": "Goalkeeper", "years": "2000-2010"},
            {"name": "Rui Costa", "position": "Midfielder", "years": "2001-2006"}
        ]
    },
    {
        "name": "Inter de Milão",
        "players": [
            {"name": "Javier Zanetti", "position": "Defender", "years": "1995-2014"},
            {"name": "Ronaldo Nazário", "position": "Forward", "years": "1997-2002"},
            {"name": "Luís Figo", "position": "Midfielder", "years": "2005-2009"},
            {"name": "Diego Milito", "position": "Forward", "years": "2009-2014"},
            {"name": "Wesley Sneijder", "position": "Midfielder", "years": "2009-2013"},
            {"name": "Samuel Eto'o", "position": "Forward", "years": "2009-2011"},
            {"name": "Esteban Cambiasso", "position": "Midfielder", "years": "2004-2014"},
            {"name": "Julio César", "position": "Goalkeeper", "years": "2005-2012"},
            {"name": "Marco Materazzi", "position": "Defender", "years": "2001-2011"},
            {"name": "Dejan Stanković", "position": "Midfielder", "years": "2004-2013"},
            {"name": "Iván Córdoba", "position": "Defender", "years": "2000-2012"}
        ]
    }
]

# Endpoint para buscar todos os clubes
@app.get("/clubs")
async def read_all_clubs():
    return CLUBS

# Endpoint para buscar um clube pelo nome
@app.get("/clubs/{club_name}")
async def read_club_by_name(club_name: str):
    for club in CLUBS:
        if club["name"].casefold() == club_name.casefold():
            return club
    return {"error": "Club not found"}

# Endpoint para buscar jogadores de um clube por posição (opcional)
@app.get("/clubs/{club_name}/players")
async def read_players_by_club_and_position(club_name: str, position: Optional[str] = None):
    print(f"Searching for club: {club_name}")  # Depuração
    print(f"Searching for position: {position}")  # Depuração

    club_found = None
    for club in CLUBS:
        if club["name"].casefold() == club_name.casefold():
            club_found = club
            break

    if not club_found:
        return {"error": "Club not found"}

    players_to_return = []
    for player in club_found["players"]:
        print(f"Checking player: {player}")  # Depuração
        if position is None or player["position"].casefold() == position.casefold():
            players_to_return.append(player)

    print(f"Players found: {players_to_return}")  # Depuração
    return players_to_return

# Endpoint para adicionar um novo jogador a um clube
@app.post("/clubs/{club_name}/add_player")
async def add_player_to_club(club_name: str, player=Body()):
    for club in CLUBS:
        if club["name"].casefold() == club_name.casefold():
            club["players"].append(player)
            return {"message": "Player added successfully", "club": club}
    return {"error": "Club not found"}

# Endpoint para atualizar um jogador de um clube
@app.put("/clubs/{club_name}/update_player")
async def update_player_in_club(club_name: str, updated_player=Body()):
    for club in CLUBS:
        if club["name"].casefold() == club_name.casefold():
            for i, player in enumerate(club["players"]):
                if player["name"].casefold() == updated_player["name"].casefold():
                    club["players"][i] = updated_player
                    return {"message": "Player updated successfully", "club": club}
            return {"error": "Player not found"}
    return {"error": "Club not found"}

# Endpoint para deletar um jogador de um clube
@app.delete("/clubs/{club_name}/delete_player/{player_name}")
async def delete_player_from_club(club_name: str, player_name: str):
    for club in CLUBS:
        if club["name"].casefold() == club_name.casefold():
            for i, player in enumerate(club["players"]):
                if player["name"].casefold() == player_name.casefold():
                    deleted_player = club["players"].pop(i)
                    return {"message": "Player deleted successfully", "player": deleted_player}
            return {"error": "Player not found"}
    return {"error": "Club not found"}