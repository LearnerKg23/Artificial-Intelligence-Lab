import torch
import torch.nn as nn
import torch.optim as optim

def run_experiment(activation_name, init_type="random", task="binary", print_results=False):
    # Set seed for reproducibility
    torch.manual_seed(42)
    
    # Dataset
    X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    if task == "binary":
        y = torch.tensor([[0.0], [1.0], [1.0], [0.0]])
        output_dim = 1
        criterion = nn.BCEWithLogitsLoss()
    else: # three-class
        y = torch.tensor([0, 1, 1, 2])
        output_dim = 3
        criterion = nn.CrossEntropyLoss()

    # Model definition
    class XORNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear1 = nn.Linear(2, 2)
            if activation_name == "sigmoid":
                self.act = nn.Sigmoid()
            elif activation_name == "tanh":
                self.act = nn.Tanh()
            elif activation_name == "relu":
                self.act = nn.ReLU()
            else:
                self.act = nn.Identity() # linear for Task 1 prediction
            
            self.linear2 = nn.Linear(2, output_dim)

        def forward(self, x):
            x = self.linear1(x)
            x = self.act(x)
            x = self.linear2(x)
            return x

    model = XORNet()

    # Initialisation
    if init_type == "zero":
        nn.init.zeros_(model.linear1.weight)
        nn.init.zeros_(model.linear1.bias)
        nn.init.zeros_(model.linear2.weight)
        nn.init.zeros_(model.linear2.bias)
        
    optimizer = optim.SGD(model.parameters(), lr=1.0)
    
    initial_loss = None
    early_grad_norm = None
    first_layer_weights = []

    # Training loop
    for step in range(2000):
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        
        if step == 0:
            initial_loss = loss.item()
            
        loss.backward()
        
        if step == 0:
            if model.linear1.weight.grad is not None:
                early_grad_norm = torch.norm(model.linear1.weight.grad).item()
                
        if init_type == "zero" and step < 5:
            first_layer_weights.append(model.linear1.weight.clone().detach())
            
        if print_results and step == 0:
            print(f"[{activation_name} - {task}] Step 0 Gradient of linear1.weight:\n{model.linear1.weight.grad}")

        optimizer.step()

    final_loss = loss.item()
    
    if task == "binary":
        probs = torch.sigmoid(model(X))
        preds = (probs > 0.5).float()
        correct = (preds == y).all().item()
    else:
        logits = model(X)
        probs = torch.softmax(logits, dim=1)
        preds = torch.argmax(probs, dim=1)
        correct = (preds == y).all().item()

    if print_results:
        print(f"\n--- Results for {activation_name} | init: {init_type} | task: {task} ---")
        print(f"Initial Loss: {initial_loss:.4f}")
        print(f"Final Loss: {final_loss:.4f}")
        print(f"Final Probabilities:\n{probs.detach()}")
        print(f"Final Predictions:\n{preds.detach()}")
        print(f"All Correct: {correct}")
        print(f"Early Grad Norm: {early_grad_norm}")
        if init_type == "zero":
            print("\nSymmetry Experiment - Linear1 Weights over first 5 steps:")
            for i, w in enumerate(first_layer_weights):
                print(f"Step {i}:\n{w}")

    return {
        "final_loss": final_loss,
        "correct": correct,
        "early_grad_norm": early_grad_norm
    }

if __name__ == "__main__":
    # Task 4A & 4B
    run_experiment("tanh", task="binary", print_results=True)
    
    # Task 4C: Symmetry
    run_experiment("tanh", init_type="zero", task="binary", print_results=True)
    
    # Task 4D: Activation experiment
    print("\n--- Task 4D: Activation Experiment ---")
    for act in ["sigmoid", "tanh", "relu"]:
        res = run_experiment(act, task="binary", print_results=False)
        print(f"{act.capitalize():<10} | Loss: {res['final_loss']:.4f} | Correct: {res['correct']} | Early Grad Norm: {res['early_grad_norm']:.4f}")
        
    # Task 5: Three-class
    print("\n--- Task 5: Three-class extension ---")
    run_experiment("tanh", task="three-class", print_results=True)
