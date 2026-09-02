from app.session import RouletteSession


print("=== Roulette Session Test ===")

session = RouletteSession()

print(session)

print("\nSession ID:")
print(session.session_id)

print("\nStatus:")
print(session.status)

print("\nInitial Spins:")
print(session.initial_spins)

print("\nAll Spins:")
print(session.spins)

print("\nStarted At:")
print(session.started_at)

print("\nEnded At:")
print(session.ended_at)